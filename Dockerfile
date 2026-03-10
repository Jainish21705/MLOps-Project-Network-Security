FROM python:3.10-slim-buster

WORKDIR /app

# Install AWS CLI
RUN apt update -y && apt install awscli -y

# Copy requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application
COPY . .

CMD ["python", "app.py"]