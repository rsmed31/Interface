FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Define environment variables
ENV LOG_PATH /var/log/apache2/access.log

# Copy requirements and install dependencies
COPY requirements.dev.txt .
RUN pip install --no-cache-dir -r requirements.dev.txt

# Copy the application code
COPY . .

# Define volume for logs
VOLUME ["/var/log/apache2"]

# Expose the port for the application
EXPOSE 8000

# Set the entry point for the container
ENTRYPOINT ["python", "src/main.py"]