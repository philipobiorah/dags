from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd



default_args ={
    'owner': 'airflow',
    'depends_on_past':False,
    'start_date': datetime(2023, 12, 28),
    'email' : ["philipobiorah.cloud@gmail.com"],
    'email_on_faliure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}


with DAG('weather_dag',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:

        is_weather_api_ready = HttpSensor(
        task_id = 'is_weather_api_ready',
        http_conn_id='weathermap_api',
        endpoint='/data/2.5/weather?q=London&appid=e28fa6457642f032b61120f9864d7bf1'


        )


        extract_weather_data = SimpleHttpOperator(
        task_id = 'extract_weather_data',
        http_conn_id = 'weathermap_api',
        endpoint='/data/2.5/weather?q=London&appid=e28fa6457642f032b61120f9864d7bf1',
        method = 'GET',
        response_filter= lambda r: json.loads(r.text),
        log_response=True
        )
