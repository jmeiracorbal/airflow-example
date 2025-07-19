from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import random
import time

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'daily_data_pipeline',
    default_args=default_args,
    description='Pipeline de datos diario con múltiples tareas',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=['pipeline', 'datos', 'ejemplo'],
)

def extract_sales_data():
    """Simula extracción de datos de ventas"""
    print("Extrayendo datos de ventas...")
    time.sleep(2)  # Simula tiempo de procesamiento
    sales_data = {
        'ventas_hoy': random.randint(1000, 5000),
        'productos_vendidos': random.randint(50, 200),
        'timestamp': datetime.now().isoformat()
    }
    print(f"Datos de ventas extraídos: {sales_data}")
    return sales_data

def extract_inventory_data():
    """Simula extracción de datos de inventario"""
    print("Extrayendo datos de inventario...")
    time.sleep(1.5)  # Simula tiempo de procesamiento
    inventory_data = {
        'stock_disponible': random.randint(100, 1000),
        'productos_bajos': random.randint(5, 20),
        'timestamp': datetime.now().isoformat()
    }
    print(f"Datos de inventario extraídos: {inventory_data}")
    return inventory_data

def transform_data(**context):
    """Combina y transforma los datos extraídos"""
    print("Transformando datos...")
    
    # Obtener datos de las tareas anteriores
    ti = context['ti']
    sales_data = ti.xcom_pull(task_ids='extract_sales')
    inventory_data = ti.xcom_pull(task_ids='extract_inventory')
    
    # Simular transformación
    time.sleep(3)
    
    transformed_data = {
        'ventas': sales_data,
        'inventario': inventory_data,
        'analisis': {
            'ratio_ventas_stock': sales_data['ventas_hoy'] / inventory_data['stock_disponible'],
            'necesidad_reposicion': inventory_data['productos_bajos'] > 10
        },
        'timestamp': datetime.now().isoformat()
    }
    
    print(f"Datos transformados: {transformed_data}")
    return transformed_data

def load_warehouse(**context):
    """Simula carga en data warehouse"""
    print("Cargando datos en warehouse...")
    
    ti = context['ti']
    transformed_data = ti.xcom_pull(task_ids='transform')
    
    time.sleep(2)
    
    # Simular carga exitosa
    load_result = {
        'status': 'success',
        'records_loaded': random.randint(100, 500),
        'load_time': datetime.now().isoformat(),
        'data': transformed_data
    }
    
    print(f"Datos cargados en warehouse: {load_result}")
    return load_result

def generate_report(**context):
    """Genera reporte basado en los datos procesados"""
    print("Generando reporte...")
    
    ti = context['ti']
    warehouse_data = ti.xcom_pull(task_ids='load_warehouse')
    
    time.sleep(1)
    
    report = {
        'report_id': f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'summary': {
            'total_ventas': warehouse_data['data']['ventas']['ventas_hoy'],
            'stock_disponible': warehouse_data['data']['inventario']['stock_disponible'],
            'necesita_reposicion': warehouse_data['data']['analisis']['necesidad_reposicion']
        },
        'generated_at': datetime.now().isoformat()
    }
    
    print(f"Reporte generado: {report}")
    return report

def send_alert(**context):
    """Envía alerta basada en el reporte"""
    print("Enviando alerta...")
    
    ti = context['ti']
    report = ti.xcom_pull(task_ids='generate_report')
    
    # Simular envío de alerta
    time.sleep(1)
    
    alert_message = f"""
    🚨 ALERTA DIARIA - {datetime.now().strftime('%Y-%m-%d %H:%M')}
    
    📊 Resumen:
    - Ventas: ${report['summary']['total_ventas']}
    - Stock disponible: {report['summary']['stock_disponible']} unidades
    - Necesita reposición: {'SÍ' if report['summary']['necesita_reposicion'] else 'NO'}
    
    Reporte ID: {report['report_id']}
    """
    
    print("Alerta enviada:")
    print(alert_message)
    return alert_message

# Definir las tareas
extract_sales = PythonOperator(
    task_id='extract_sales',
    python_callable=extract_sales_data,
    dag=dag,
)

extract_inventory = PythonOperator(
    task_id='extract_inventory',
    python_callable=extract_inventory_data,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag,
)

load_warehouse_task = PythonOperator(
    task_id='load_warehouse',
    python_callable=load_warehouse,
    dag=dag,
)

generate_report_task = PythonOperator(
    task_id='generate_report',
    python_callable=generate_report,
    dag=dag,
)

send_alert_task = PythonOperator(
    task_id='send_alert',
    python_callable=send_alert,
    dag=dag,
)

# Definir el flujo de dependencias
[extract_sales, extract_inventory] >> transform >> load_warehouse_task >> generate_report_task >> send_alert_task 