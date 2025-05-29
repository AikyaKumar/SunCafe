# FROM python:3.9
# WORKDIR /app
# COPY producer.py .
# RUN pip install kafka-python
# CMD ["python", "producer.py"]

# producer/Dockerfile
FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install kafka-python requests

CMD ["python", "producer.py"]
