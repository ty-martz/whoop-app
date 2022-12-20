# Example dag generated with ChatGPT with the prompt:
# "can you write an example apache airflow dag script in python"

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from tasks.task_one import whoop_email_task

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 12, 14),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'whoop_email_dag',
    default_args=default_args,
    schedule_interval=timedelta(hours=1),
)

# Define a function to be executed by the PythonOperator
def whoop_email():
    whoop_email_task()

# Define the task using the PythonOperator
greet_task = PythonOperator(
    task_id='daily_email',
    python_callable=whoop_email,
    dag=dag,
)
