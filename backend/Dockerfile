# Use an official Python runtime as a parent image
FROM python:3.9-slim

WORKDIR /backend

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# RUN apt-get install poppler-utils -y

RUN sh tesseract.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]