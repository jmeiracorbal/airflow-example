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
    'hola_mundo',
    default_args=default_args,
    description='DAG de ejemplo básico',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['ejemplo', 'basico'],
)

def imprimir_hola_mundo():
    print("¡Hola Mundo desde Apache Airflow!")
    return "Tarea completada exitosamente"

tarea_hola_mundo = PythonOperator(
    task_id='imprimir_hola_mundo',
    python_callable=imprimir_hola_mundo,
    dag=dag,
)

tarea_hola_mundo 