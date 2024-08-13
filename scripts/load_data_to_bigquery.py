from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os

# project ID and dataset name
project_id = 'sentiment-analysis-410608'
dataset_id = 'youtube_sentiment'

# Path to your JSON key file
json_key_path = 'sentiment-analysis.privateKey.json'

# Csv file path
videos_file = 'data/unpreprocessed/videos_metadata.csv'
comments_file = 'data/unpreprocessed/comments_metadata.csv'

# Initialize a BigQuery client
credentials = service_account.Credentials.from_service_account_file(json_key_path)
client = bigquery.Client(project=project_id, credentials=credentials)

def upload_csv_to_bq(csv_file_path, table_id):
    # Table references
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    # Define the job configuration
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1, # skip the header
        autodetect=False,
    )

    # Load data to BigQuery table
    with open(csv_file_path, 'rb') as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()

    print(f"Successfully upload {csv_file_path} to {table_id} in BigQuery")

if __name__ == "__main__":
    # upload_csv_to_bq(videos_file, 'raw_videos')
    upload_csv_to_bq(comments_file, 'raw_comments')