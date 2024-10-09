import streamlit as st
import requests
import json
import sqlite3
import uuid
from datetime import datetime

from rag import rag_function


DB_PATH ='./data/feedback.db'

# SQLite database setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table for requests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            query TEXT,
            response TEXT,
            model_name TEXT,
            created_at TEXT
        )
    ''')

    # Create table for feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            request_id TEXT,
            feedback TEXT,
            FOREIGN KEY(request_id) REFERENCES requests(id)
        )
    ''')

    # Create table for feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            request_id TEXT,            
            prompt_length INT,
            total_duration INT,
            load_duration INT,
            prompt_eval_duration INT,
            eval_count INT,
            eval_duration INT,
            created_at TEXT,
            FOREIGN KEY(request_id) REFERENCES requests(id)
        )
    ''')

    conn.commit()
    conn.close()

# Function to store query and response in the requests table
def store_request(query, response, model_name, meta):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Generate a unique ID and timestamp
    request_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    # model_response = response["response"]
    # model_name = response["model"]
    print(" query, response:  ", query, response, model_name)
    
    # Insert query, response, and timestamp into the requests table
    cursor.execute('''
        INSERT INTO requests (id, query, response, model_name, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (request_id, query, response, model_name,  timestamp))

    prompt_length = meta["prompt_length"]
    total_duration = meta["total_duration"]
    load_duration = meta["load_duration"]
    prompt_eval_duration = meta["prompt_eval_duration"]
    eval_count = meta["eval_count"]
    eval_duration = meta["eval_duration"]
    print( (  request_id, 
            prompt_length,
            total_duration,
            load_duration,
            prompt_eval_duration,
            eval_count,
            eval_duration,
        ))
    cursor.execute('''
        INSERT INTO performance_metrics (request_id, prompt_length, total_duration, load_duration, prompt_eval_duration, eval_count, eval_duration, created_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (  request_id, 
            prompt_length,
            total_duration,
            load_duration,
            prompt_eval_duration,
            eval_count,
            eval_duration,
            timestamp
        ))
    
    conn.commit()
    conn.close()

    return request_id

# Function to store feedback (thumb up or thumb down)
def store_feedback(request_id, feedback_type):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert feedback into the feedback table
    cursor.execute('''
        INSERT INTO feedback (request_id, feedback)
        VALUES (?, ?)
    ''', (request_id, feedback_type))

    conn.commit()
    conn.close()
    print("updated feedback")


if __name__ == '__main__':
    # Initialize the database
    init_db()

    # Initialize session state for request_id and feedback
    if 'request_id' not in st.session_state:
        st.session_state['request_id'] = None
    if 'response' not in st.session_state:
        st.session_state['response'] = None
    if 'query' not in st.session_state:
        st.session_state['query'] = None

    # Streamlit UI
    st.title("RAG-based SQL Query Helper")
    model_list = [
        "deepseek-coder-v2:16b",
        "llama3.2:1b",
        "llama3.2:latest",
        "qwen2:1.5b",
        "phi3.5:latest",
        "nemotron-mini:latest"
    ]

    # Input form for user query and model selection
    with st.form(key="rag_form"):
        query = st.text_input("Enter your query:", value="What is the total number of hospital beds in each state?")
        model_name = st.selectbox("Select a model", model_list)
        submit_button = st.form_submit_button(label="Generate Answer")
        
    # If the form is submitted
    if submit_button:
        if query:
            with st.spinner('Retrieving context and generating response...'):
                # Call the RAG function and get the streaming response generator
                response_generator = rag_function(query, model_name)
                
                placeholder = st.empty()

                model_response = ""

                # Display the response as it streams
                for part in response_generator:
                    # print(part)
                    # Update the request with the current part of the response
                    model_response += part["response"]
                    placeholder.write(model_response)  # Display the streaming response
                    done=part["done"]
                    if done:
                        meta = {
                            "prompt_length": len(part["context"]),
                            "total_duration": part["total_duration"],
                            "load_duration": part["load_duration"],
                            "prompt_eval_duration": part["prompt_eval_duration"],
                            "eval_count": part["eval_count"],
                            "eval_duration": part["eval_duration"]
                        }
                        st.session_state['meta'] = meta

                st.session_state['response'] = model_response
                # Store the query and response in the database (initially empty)
                request_id = store_request(query, model_response, model_name, meta)
                # Save the final response to session state
                st.session_state['request_id'] = request_id
                st.session_state['query'] = query

    # If there is a stored request and response in session state
    if st.session_state['response']:
        # Display the saved response
        st.subheader("Generated Response:")
        st.write(st.session_state['response'])

        # Feedback buttons (Thumbs up and Thumbs down)
        st.subheader("Was this response helpful?")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("👍 Yes"):
                store_feedback(st.session_state['request_id'], "thumbs_up")
                st.success("Thank you for your feedback!")

        with col2:
            if st.button("👎 No"):
                store_feedback(st.session_state['request_id'], "thumbs_down")
                st.success("Thank you for your feedback!")
