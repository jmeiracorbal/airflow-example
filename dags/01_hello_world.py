from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'hello_world',
    default_args=default_args,
    description='DAG from basic example',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['basic_example', 'hello_world'],
)

def print_hello_world():
    print("Hello World from Apache Airflow!")
    return "Task completed successfully"

task_hello_world = PythonOperator(
    # using a task_id to identify the task
    task_id='print_hello_world',
    # with python_callable we call to the function that we defined preivously
    python_callable=print_hello_world,
    dag=dag,
)

# The airflow scheduler exewcutes this task the task_hello_world task
task_hello_world