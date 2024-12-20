FROM python:3.12-slim

WORKDIR /app

COPY requirements.dev.txt .

RUN pip install --no-cache-dir -r requirements.dev.txt

COPY . .

EXPOSE 8000

CMD ["python", "src/main.py"]
