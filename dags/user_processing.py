from jsonschema import validate
from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.email import EmailOperator
from json_schema import json_std_schema

import json
from pandas import json_normalize
from datetime import datetime

@task
def validate_user_schema(data):
    try:
        validate(data, json_std_schema)
        return 'JSON schema OK'
    except Exception as e:
        # send_email()
        raise ValueError('JSON schema check failed')

@task
def check_data():
    hook = PostgresHook(postgres_conn_id='postgres')
    records = hook.get_records('SELECT COUNT(*) FROM users')
    if len(records) < 1 or len(records[0]) < 1:
        # send_email()
        raise ValueError('Data quality check failed: no records found')

@task
def process_user(user):
    user = user['results'][0]
    processed_user = json_normalize({
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
    })
    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)

@task
def store_user():
    hook = PostgresHook(postgres_conn_id='postgres')
    hook.copy_expert(
        sql="COPY users FROM stdin WITH DELIMITER as ','",
        filename='/tmp/processed_user.csv'
    )

# def send_email():
#     return EmailOperator(
#         task_id='send_email',
#         to='mesesan_ovidiu@yahoo.com',
#         subject='Data quality check failed',
#         html_content='The data quality check task failed. Please investigate.'
#     )
        
default_args = {
    "catchup": False,
    "email":["mesesan_ovidiu@yahoo.com"],
    "email_on_retry":False,
    "email_on_failure":False}

with DAG('user_processing', start_date = datetime(2021, 1, 1), schedule_interval='* * * * *', default_args=default_args) as dag:

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        '''
    )

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )

    extract_user = SimpleHttpOperator(
        task_id='extract_user',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    validated_user_schema = validate_user_schema(extract_user.output)
    processed_user = process_user(extract_user.output)
    stored_user = store_user()
    check_datas = check_data()

    create_table >> is_api_available >> extract_user >> processed_user >> stored_user >> check_datas
    create_table >> is_api_available >> extract_user >> validated_user_schema
