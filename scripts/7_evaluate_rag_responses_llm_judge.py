# Step 2: Apply LLM Judge to the Responses and Store Judgements

import pandas as pd
import json
import tqdm

def judge_the_response(query, response, judge_model):
    judge_prompt = f"User Query: {query}\n\nModel Response: {response}\n\n" \
                "Now, evaluate the user query and model response and classify as Relevant, Neutral, or Non_Relevant." \
                "Give appropriate response in one word against the key 'classification'."
    
    response_generator = call_llm(judge_prompt, judge_model, True)
    model_response = ''.join([part["response"] for part in response_generator])
    classification = json.loads(model_response.lower())["classification"]
    return classification

if __name__ == '__main__':
    
    ## select model to use as a judge
    # model = "deepseek-coder-v2:16b"
    model = "llama3.2:1b"
    # model = "llama3.2:latest"
    # model = "qwen2:1.5b"
    # model = "phi3.5:latest"

    # Load the RAG responses from CSV        
    rag_responses_file = f'../output/rag_responses_{model}.csv'
    df = pd.read_csv(rag_responses_file)

    judge_model = "deepseek-coder-v2:16b"
    judgements = []

    # Apply LLM judge to each response
    for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        try:
            query = row['query']
            model_response = row['model_response']

            # Get judgement for the response
            judgement = judge_the_response(query, model_response, judge_model)
            judgements.append(judgement)
            print(f"Record {index}: Judgement - {judgement}")

        except Exception as e:
            print(f"Error processing record {index}: {e}")
    
    # Add the judgements to the dataframe
    df['judgement'] = judgements

    # Save the judgements to a new CSV file
    df.to_csv('rag_responses_with_judgements.csv', index=False)
    print("Judgements saved to rag_responses_with_judgements.csv")

    # Count the classifications
    relevant_count = judgements.count("relevant")
    neutral_count = judgements.count("neutral")
    non_relevant_count = judgements.count("non_relevant")

    # Total number of records processed
    total_records = len(judgements)

    # Print the summary of judgements
    print(f"Relevant        : {relevant_count}/{total_records}")
    print(f"Neutral         : {neutral_count}/{total_records}")
    print(f"Non_Relevant    : {non_relevant_count}/{total_records}")
