import pandas as pd
from elasticsearch import Elasticsearch
import json
import tqdm

from injestion_utils import read_hf_dataset



# Function to index data into Elasticsearch
def index_record(es, index_name, doc_id, record):
    es.index(index=index_name, id=doc_id, document=record)




if __name__ == '__main__':
    # Elasticsearch connection (assumes it's running on localhost:9200)
    es = Elasticsearch(
        hosts=['http://localhost:9200']
    )
    #     hosts=[{'host': 'localhost', 'port': 9200}],
    #     scheme='http'
    # )
    # es = Elasticsearch("http://localhost:9200/")
    # es = Elasticsearch(
    #     hosts=['http://localhost:9200'],
    #     timeout=30  # Increase the timeout value (in seconds)
    # )
    # Example usage of reading parquet file
    dataset_path = './synthetic_text_to_sql_local'  # Replace with your Parquet file path
    df = read_hf_dataset(dataset_path)
    print(df)

    # Example JSON record
    record = {
        "id": 39325,
        "domain": "public health",
        "domain_description": "Community health statistics, infectious disease tracking data, healthcare access metrics, and public health policy analysis.",
        "sql_complexity": "aggregation",
        "sql_complexity_description": "aggregation functions (COUNT, SUM, AVG, MIN, MAX, etc.), and HAVING clause",
        "sql_task_type": "analytics and reporting",
        "sql_task_type_description": "generating reports, dashboards, and analytical insights",
        "sql_prompt": "What is the total number of hospital beds in each state?",
        "sql_context": "CREATE TABLE Beds (State VARCHAR(50), Beds INT); INSERT INTO Beds (State, Beds) VALUES ('California', 100000), ('Texas', 85000), ('New York', 70000);",
        "sql": "SELECT State, SUM(Beds) FROM Beds GROUP BY State;",
        "sql_explanation": "This query calculates the total number of hospital beds in each state in the Beds table. It does this by using the SUM function on the Beds column and grouping the results by the State column."
    }

    # Index the record into Elasticsearch
    index_name = 'sql_records'
    doc_id = record["id"]
    index_record(es, index_name, doc_id, record)

    # # Optionally, index records from the parquet file into Elasticsearch
    for index, row in tqdm.tqdm(df.iterrows()):
        record = row.to_dict()
        doc_id = record.get('id', index)  # Use 'id' from data or fallback to index
        index_record(es,index_name, doc_id, record)
