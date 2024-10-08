# sql-rag
LLM-powered Auto SQL Query Writer with Retrieval-Augmented Generation (RAG)

## Project Description:

The LLM-powered Auto SQL Query Writer with Retrieval-Augmented Generation (RAG) is an AI-based system designed to automatically generate SQL queries based on natural language inputs. The project leverages large language models (LLMs) in conjunction with a RAG framework to dynamically retrieve relevant information, ensuring accurate and contextually appropriate query generation.

This system enables users, even those without technical expertise, to interact with databases by simply describing their data requirements in plain language. The LLM processes the input, while the RAG mechanism retrieves database schema details, past queries, and related context to ensure the generated SQL queries are correct, optimized, and specific to the given database structure.
Key Features:

    Natural Language to SQL Conversion: Converts user queries written in natural language into executable SQL commands.
    Retrieval-Augmented Generation (RAG): Enhances query accuracy by retrieving schema information, previous queries, and relevant documentation before generating SQL.
    Dynamic Adaptability: Adapts to various database schemas and data models, allowing for application across different industries and database setups.
    Error Handling and Optimization: Automatically detects potential query errors and provides optimized solutions to ensure efficient data retrieval.
    User-Friendly Interface: Easy-to-use interface where non-technical users can input their requests and get SQL queries instantly, streamlining the workflow.
    Customizability: Users can specify advanced options, such as JOIN conditions, filters, and aggregation functions, for more complex queries.

Use Cases:

    Business Intelligence: Teams can extract insights from databases without needing deep SQL expertise, accelerating decision-making.
    Data Engineering: Assists engineers in generating complex SQL queries for data extraction and analysis.
    Database Management: Simplifies tasks such as data querying, reporting, and analysis for administrators managing large-scale databases.

By combining the power of LLMs and RAG, this project provides a robust solution for automated SQL query generation, reducing manual intervention, improving efficiency, and broadening access to database querying capabilities across different user levels.


## Dataset 
https://huggingface.co/datasets/gretelai/synthetic_text_to_sql


## Setup


run the whole env
```bash
cd docker
docker-compose up
```


## running individual services

To run Elasticsearch:
```bash
docker-compose -f docker-compose.yml up
```

To run Kibana:
```bash
docker-compose -f docker-compose.kibana.yml up
```

To run Grafana:
```bash
docker-compose -f docker-compose.grafana.yml up
```

To run Streamlit:
```bash
docker-compose -f docker-compose.streamlit.yml up
```

# running scripts

create python env
```bash
python -m venv envname
source activate envname/bin/activate
```

install dependencies
```bash
pip install -r requirements.txt
```

download the dataset
```bash
python scripts/1_download_data.py
```

verify dataset
```bash
python scripts/2_print_data.py
```

load dataset
```bash
python scripts/3_ingestion_script.py
```