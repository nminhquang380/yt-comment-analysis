import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import numpy as np

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve environment variables
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')

def connect_to_snowflake():
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    return conn

def load_data_to_snowflake(conn, df, table):
    # cursor = conn.cursor()
    # for row in df.itertuples(index=False, name=None):
    #     cursor.execute(f"INSERT INTO {table} VALUES", row)
    # conn.commit()
    # cursor.close()

    write_pandas(
        conn=conn,
        df=df,
        table_name=table,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )

def main():
    # Read data from CSV files
    videos_metadata_df = pd.read_csv('/home/micasidad/Desktop/yt-comment-analysis/data/unpreprocessed/videos_metadata.csv')
    video_comments_df = pd.read_csv('/home/micasidad/Desktop/yt-comment-analysis/data/unpreprocessed/comments_metadata.csv')

    # Connect to Snowflake
    conn = connect_to_snowflake()

    # Load data into Snowflake
    load_data_to_snowflake(conn, videos_metadata_df, 'RAW_VIDEOS')
    load_data_to_snowflake(conn, video_comments_df, 'RAW_COMMENTS')

    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()
