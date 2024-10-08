from app.rag import search, elastic_search, call_llm

import pandas as pd
import json
import tqdm



# Reading a Parquet file and displaying its contents
def read_parquet(file_path):
    df = pd.read_parquet(file_path)
    return df


if __name__ == '__main__':
    
    # Example usage of reading parquet file
    parquet_file = './data/synthetic_text_to_sql/synthetic_text_to_sql_train.snappy.parquet'  # Replace with your Parquet file path
    df = read_parquet(parquet_file)
    # print(df)

    result_count = 0

    # # Optionally, index records from the parquet file into Elasticsearch
    for index, row in tqdm.tqdm(df.iterrows()):
        record = row.to_dict()
        doc_id = record.get('id', index)  # Use 'id' from data or fallback to index
        # index_record(es,index_name, doc_id, record)
        # print("record : ", record)
        
        query = record["sql_prompt"]
        gt_sql = record["sql"]

        results = elastic_search(query)
        value_result = (results[0]["sql"] == gt_sql)
        print(f"result: {value_result} query: {query} gt_sql: {gt_sql}")

        result_count += int(value_result)
    print(f"result {result_count}/{len(df)}")
