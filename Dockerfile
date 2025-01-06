FROM python:3.12-slim

WORKDIR /app

ENV LOG_PATH /var/log/apache2/access.log

COPY requirements.dev.txt .

RUN pip install --no-cache-dir -r requirements.dev.txt

COPY . .

VOLUME ["/"]

EXPOSE 8000

CMD ["python", "src/main.py"]