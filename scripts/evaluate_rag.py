from rag import rag_function, call_llm

import pandas as pd
import json
import tqdm



# Reading a Parquet file and displaying its contents
def read_parquet(file_path):
    df = pd.read_parquet(file_path)
    return df

def judge_the_response(query, response, judge_model):
    # prompt = f"""
    # Evaluate the following query and response:
    #     Query: {query}
    #     Response: {response}
    #     Classify the response as: relevant, neutral, or non_relevant give the output.
    # """
    judge_prompt = f"User Query: {query}\n\nModel Response: {response}\n\n" \
                "Now, evaluate the user query and model response and classify as Relevant, Neutral, or Non_Relevant." \
                "Give appropriate response in one word against the key 'classification' ."

    print(f"judge_prompt {judge_prompt}")
    response_generator = call_llm(judge_prompt, judge_model, True)
    model_response = [ part["response"] for part in response_generator]
    print("--- ",model_response)
    model_response = ''.join(model_response)
    classification = json.loads(model_response.lower())["classification"]
    return classification



if __name__ == '__main__':
    
    # Example usage of reading parquet file
    parquet_file = './data/synthetic_text_to_sql/synthetic_text_to_sql_train.snappy.parquet'  # Replace with your Parquet file path
    df = read_parquet(parquet_file)
    # print(df)

    model = "deepseek-coder-v2:16b"
    # model = "llama3.2:1b"
    # model = "llama3.2:latest"
    # model = "qwen2:1.5b"
    # model = "phi3.5:latest"
    # model = "nemotron-mini:latest"
    
    judge_model = "deepseek-coder-v2:16b"
    # judge_model = "llama3.2:1b"
    # judge_model = "llama3.2:latest"
    # judge_model = "qwen2:1.5b"
    # judge_model = "phi3.5:latest"
    # judge_model = "nemotron-mini:latest"

    judgements =[]


    # # Optionally, index records from the parquet file into Elasticsearch
    for index, row in tqdm.tqdm(df.iterrows()):
        try:
            record = row.to_dict()
            doc_id = record.get('id', index)  # Use 'id' from data or fallback to index
            # index_record(es,index_name, doc_id, record)
            # print("record : ", record)
            
            query = "Give me the query of "+ record["sql_prompt"]
            gt_sql = record["sql"]

            response_generator = rag_function(query, model)
            model_response = ''.join([ part["response"] for part in response_generator])
            print(f"--- {model_response}")
            model_response = json.loads(model_response)
            
            # print(model_response)        
            print("model response: ",model_response)
        
            

            judgement = judge_the_response(query, model_response, judge_model)
            judgements.append(judgement)
            print(f"judgement: {judgement}")
            print()
        except Exception as e:
            print(e)
            

       
    length_of_array =len(df)
    print(f"relevant        : {judgements.count("relevant")}/{len(judgements)}      |{length_of_array}")
    print(f"neutral         : {judgements.count("neutral")}/{len(judgements)}       |{length_of_array}")
    print(f"non_relevant    : {judgements.count("non_relevant")}/{len(judgement)}   | {length_of_array}")
