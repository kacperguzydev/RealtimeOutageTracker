FROM python:3.11-slim

LABEL authors="hyuhi"

# Install system dependencies: OpenJDK 17 JRE headless, wget, unzip, and netcat-openbsd (for wait-for-it.sh)
RUN apt-get update && \
    apt-get install -y openjdk-17-jre-headless wget unzip netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the wait-for-it script and set execute permission
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . /app

# Expose port 8501 for Streamlit
EXPOSE 8501

# Default command
CMD ["python", "main.py"]
