# Use Python 3.11 slim as our base (Efficient & Secure)
FROM python:3.11-slim

# Set environment variables to ensure output is logged immediately
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the mission code
COPY . .

# Cloud Run expects the app to listen on port 8080
EXPOSE 8080

# Command to run the dashboard
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]