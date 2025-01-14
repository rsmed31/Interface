FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

VOLUME ["/app/logs"]

# Expose the port for the application
EXPOSE 8080

# Set the entry point for the container to pass arguments
ENTRYPOINT ["python", "src/main.py"]