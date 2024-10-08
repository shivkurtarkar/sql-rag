import requests
import json

import uuid
from datetime import datetime
from elasticsearch import Elasticsearch


# Search function that retrieves relevant data (simulated here with a simple example)
def search(query):
    search_results = {
        "What is the total number of hospital beds in each state?": {
            "sql_context": "CREATE TABLE Beds (State VARCHAR(50), Beds INT); "
                       "INSERT INTO Beds (State, Beds) VALUES ('California', 100000), "
                       "('Texas', 85000), ('New York', 70000);",
            "sql": "SELECT State, SUM(Beds) FROM Beds GROUP BY State;",
            "sql_explanation": "This query calculates the total number of hospital beds in each state in the Beds table."
        }
    }
    tmpQuery= "What is the total number of hospital beds in each state?"
    return search_results.get(tmpQuery, None)

# Search function that retrieves relevant data (simulated here with a simple example)
def elastic_search(query):
    es_client = Elasticsearch(
        hosts=['http://localhost:9200']
    )

    # Define the search body
    search_query = {
        "size":1,
        "query": {
            "multi_match": {
                "query": query,
                "fields": [
                    "domain",
                    "domain_description",
                    "sql_complexity",
                    "sql_complexity_description",
                    "sql_task_type",
                    "sql_task_type_description",
                    "sql_prompt",
                    "sql_context",
                    "sql",
                    "sql_explanation"
                ]
            }
        }
    }
    
    index="sql_records"

    response = es_client.search(index=index, body=search_query)
        
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    # Return the search results
    return result_docs


# Function to call the Ollama model and return a generator for streaming responses
def call_llm(prompt, model, stream=False):
    url = "http://localhost:11434/api/generate"  # Ollama server URL
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,  # Set to True for streaming response
        "format": "json"   # Ensure response is structured as JSON
    }

    try:
        # Make the POST request
        response = requests.post(url, json=payload, stream=stream)
        response.raise_for_status()  # Raise an error for bad responses

        if stream:
            for line in response.iter_lines():
                if line:
                    data = line.decode('utf-8')
                    try:
                        # print(data)
                        json_data = json.loads(data)
                        # part_response = json_data['response']
                        # yield part_response  # Yield each part of the response
                        yield json_data
                    except json.JSONDecodeError:
                        print("Error decoding JSON:", data)
        else:
            # If not streaming, return the full response
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        yield "Error occurred while calling the model."

# RAG function that combines search and LLM
def rag_function(query, model_name):
    # search_result = search(query)
    search_results = elastic_search(query)
    print("search_result :",search_results)

    if search_results and len(search_results) >0:
        search_result = search_results[0]
        augmented_prompt = f"User Query: {query}\n\nContext: {search_result['sql_context']}\n\n" \
                           f"SQL Query: {search_result['sql']}\n\n" \
                           f"Explanation: {search_result['sql_explanation']}\n\n" \
                           "Now, please generate an appropriate response."

        return call_llm(augmented_prompt, model_name, stream=True)  # Return generator
    else:
        return iter(["No relevant search results found for the query."])  # Return an iterator
