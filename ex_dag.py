# Example dag generated with ChatGPT with the prompt:
# "can you write an example apache airflow dag script in python"

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 12, 14),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'example_dag',
    default_args=default_args,
    schedule_interval=timedelta(hours=1),
)

# Define a function to be executed by the PythonOperator
def greet():
    print('Hello, World!')

# Define the task using the PythonOperator
greet_task = PythonOperator(
    task_id='greet_task',
    python_callable=greet,
    dag=dag,
)
