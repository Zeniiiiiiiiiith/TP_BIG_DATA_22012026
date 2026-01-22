from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="ingest_csv_to_bronze_silver",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    run_spark = BashOperator(
        task_id="run_spark_batch",
        bash_command=(
            "spark-submit "
            "--master spark://spark-master:7077 "
            "/opt/spark/jobs/batch_csv_to_silver.py"
        ),
    )

    run_spark
