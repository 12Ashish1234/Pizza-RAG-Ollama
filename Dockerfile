# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
# build-essential might be needed for some python packages like chromadb/hnswlib
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Define environment variable
# This can be overridden by docker-compose or run command
ENV OLLAMA_BASE_URL="http://host.docker.internal:11434"

# Run server.py as a module when the container launches
CMD ["python", "-m", "src.server"]
