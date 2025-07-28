from airflow import DAG # type: ignore
from airflow.operators.bash import BashOperator # type: ignore
from datetime import datetime, timedelta

default_args = {
    'owner': 'balaji',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='shopwise_etl_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # or use None to trigger manually
    catchup=False
) as dag:

    transform_task = BashOperator(
        task_id='transform_raw_data',
        bash_command='python /opt/airflow/scripts/transform.py'
    )

    load_task = BashOperator(
        task_id='load_cleaned_to_postgres',
        bash_command='python /opt/airflow/scripts/load_to_postgres.py'
    )

    transform_task >> load_task
