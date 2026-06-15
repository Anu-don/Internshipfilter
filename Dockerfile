FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/results

CMD ["python", "app.py"]