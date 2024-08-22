#!/bin/bash

# Run Python scripts
python scripts/extract_youtube_data.py
python scripts/preprocess_data.py
python scripts/load_data_to_bigquery.py

# Change directory to dbt and run dbt commands
cd dbt
dbt run
