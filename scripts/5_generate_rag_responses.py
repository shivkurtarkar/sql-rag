# Step 1: Generate RAG Responses and Store Them

import pandas as pd
import json
import tqdm

from app.rag import rag_function

# Reading a Parquet file and displaying its contents
def read_parquet(file_path):
    df = pd.read_parquet(file_path)
    return df

if __name__ == '__main__':
    
    # Example usage of reading parquet file
    parquet_file = './data/synthetic_text_to_sql/synthetic_text_to_sql_train.snappy.parquet'  # Replace with your Parquet file path
    df = read_parquet(parquet_file)
    df = df[:1000]
    # model = "deepseek-coder-v2:16b"
    model = "llama3.2:1b"
    # model = "llama3.2:latest"
    # model = "qwen2:1.5b"
    # model = "phi3.5:latest"

    output_data = []

    # Generate RAG responses and store them
    for index, row in tqdm.tqdm(df.iterrows(), total=df.shape[0]):
        try:
            record = row.to_dict()
            doc_id = record.get('id', index)  # Use 'id' from data or fallback to index
            query = "Give me the query of " + record["sql_prompt"]
            gt_sql = record["sql"]

            # Generate response using the RAG model
            response_generator = rag_function(query, model)
            model_response = ''.join([part["response"] for part in response_generator])

            output_data.append({
                "id": doc_id,
                "query": query,
                "ground_truth_sql": gt_sql,
                "model_response": model_response
            })
        
        except Exception as e:
            print(f"Error processing record {index}: {e}")

    # Save the RAG responses to a CSV file
    output_df = pd.DataFrame(output_data)
    output_df.to_csv(f'rag_responses_{model}.csv', index=False)
    print("RAG responses saved to rag_responses.csv")
