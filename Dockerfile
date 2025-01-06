FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Define default environment variable for log path
ENV  LOG_PATH /app/logs/access.log

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

VOLUME ["/app/logs"]

# Expose the port for the application
EXPOSE 8000

# Set the entry point for the container to pass arguments
ENTRYPOINT ["python", "src/main.py"]