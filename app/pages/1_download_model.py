import streamlit as st
import requests
import json



# Function to pull model from Ollama server
def pull_model(model_name):
    url = "http://localhost:11434/api/pull"  # Ollama server URL
    payload = {
        "name": model_name
    }

    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        # Initialize the Streamlit progress bar
        progress_text = "Operation in progress. Please wait."
        progress_bar = st.progress(0, text=progress_text)

        # Process the streaming response
        for line in response.iter_lines():
            if line:
                # Decode and load the JSON response
                data = line.decode('utf-8')
                try:
                    json_data = json.loads(data)
                    total = json_data.get("total", 0)
                    completed = json_data.get("completed", 0)
                    digest = json_data.get("digest", "")


                    # Convert bytes to MB
                    total_mb = total / (1024 * 1024)
                    completed_mb = completed / (1024 * 1024)

                    # Update the progress bar based on total and completed
                    if total > 0:
                        progress = completed / total
                        progress_bar.progress(progress, text=f"Downloaded Digest: {digest} {completed_mb:.2f} MB of {total_mb:.2f} MB")

                except json.JSONDecodeError:
                    st.warning("Error decoding JSON: " + data)

        # Finalize progress to 100%
        progress_bar.progress(1.0, text="Download complete!")
        st.success(f"Model '{model_name}' has been downloaded.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")


if __name__=="__main__":

    # List of available models
    model_list = [
        "deepseek-coder-v2:16b",
        "llama3.2:1b",
        "llama3.2:latest",
        "qwen2:1.5b",
        "phi3.5:latest",
        "nemotron-mini:latest"
    ]
    # Streamlit UI
    st.title("Ollama Model Downloader")
    st.write("Download model to be used in for rag")
    # Dropdown menu for model selection
    model_name = st.selectbox("Select a model:", model_list)

    if st.button("Download"):
        with st.spinner("Downloading..."):
            pull_model(model_name)  # Call the function without needing to capture a return value

    # # Rerun button
    # if st.button("Rerun"):
    #     st.experimental_rerun()
