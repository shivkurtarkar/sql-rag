# Base image with Python 3.9
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory (where the Streamlit app is located) to the working directory
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "rag_streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
