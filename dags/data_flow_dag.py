import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import your functions from the scripts
from scripts.extract_youtube_data import main as extract_data_main
from scripts.preprocess_data import main as preprocess_data_main
from scripts.load_data_to_bigquery import main as put_data_to_bigquery_main

# Define your DAG
with DAG(
    dag_id='python_scripts_dag',
    start_date=pendulum.datetime(2024, 8, 31),  # Set the specific start date to 31st August 2024
    schedule_interval='@weekly',  # Adjust this as per your requirements
    catchup=False,
) as dag:

    # Task 1: Extract Data
    extract_data_task = PythonOperator(
        task_id='extract_data_task',
        python_callable=extract_data_main,
    )

    # Task 2: Preprocess Data
    preprocess_data_task = PythonOperator(
        task_id='preprocess_data_task',
        python_callable=preprocess_data_main,
    )

    # Task 3: Put Data to BigQuery
    put_data_to_bigquery_task = PythonOperator(
        task_id='put_data_to_bigquery_task',
        python_callable=put_data_to_bigquery_main,
    )

    # Define task dependencies
    extract_data_task >> preprocess_data_task >> put_data_to_bigquery_task
