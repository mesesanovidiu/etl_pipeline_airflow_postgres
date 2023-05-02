FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./dags/user_processing.py", "./unittest/unittesting.py", "./dags/json_schema.py"]
