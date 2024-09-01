import os
import json
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
import logging

HOME = os.environ["HOME"]  # retrieve the location of your home folder
manifest_path = os.path.join(HOME, "gcs/data/target/manifest.json")  # Adjust path if necessary

with open(manifest_path) as f:  # Open manifest.json
    manifest = json.load(f)  # Load its contents into a Python Dictionary
    nodes = manifest["nodes"]  # Extract just the nodes

# Build an Airflow DAG
with DAG(
    dag_id="dbt_bigquery",  # The name that shows up in the UI
    start_date=pendulum.datetime(2024, 8, 31),  # Set the specific start date to 31st August 2024
    schedule_interval='@weekly',
    catchup=False,
) as dag:

    # Create a dict of Operators for model nodes only
    dbt_tasks = {
        node_id: BashOperator(
            task_id=".".join(
                [node_info["resource_type"], node_info["package_name"], node_info["name"]]
            ),
            bash_command="dbt run --models " + f"{node_info['name']} --target dev"
        )
        for node_id, node_info in nodes.items() if node_info["resource_type"] == "model"
    }

    # Define relationships between Operators
    for node_id, node_info in nodes.items():
        if node_info["resource_type"] == "model":
            upstream_nodes = node_info["depends_on"]["nodes"]
            if upstream_nodes:
                for upstream_node in upstream_nodes:
                    if upstream_node in dbt_tasks:
                        dbt_tasks[upstream_node] >> dbt_tasks[node_id]
                    else:
                        logging.warning(f"Upstream node {upstream_node} not found in dbt_tasks")

if __name__ == "__main__":
    dag.cli()
