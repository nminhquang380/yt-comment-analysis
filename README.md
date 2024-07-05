# Sentiment Analysis on YouTube Comments

## Introduction
This project is a sentiment analysis on YouTube comments from a specific channel. The channel I aim to analyze is Joma Tech, a Programmer Vlogger that I like. The ultimate result would be a dashboard using **Tableau**.

First, I will load the data by YouTube API to Snowflake as a Data Warehouse. I will have 2 initial tables: Videos and Comments. Then I will pre-process the data and transform it using dbt, in which I will create a table for users who comment and employ Sentiment Analysis Model such as Vader or TextBlob to estimate the sentiment score of each comment. From there, I will use Tableau or Power BI to create a Dashboard and publish it.

The project also leverages Airflow to build an automated pipeline.

## Project Plan

### 1. Data Extraction

#### a. Set up YouTube Data API
1. Create a project on the Google Developer Console.
2. Enable the YouTube Data API v3.
3. Generate API credentials (API key).

#### b. Extract Data from YouTube
1. Use the YouTube Data API to extract relevant data, including video details and comments.
2. Save the extracted data in JSON format.

### 2. Data Loading

#### a. Snowflake Setup
1. Create a Snowflake account and configure the necessary database, schema, and tables.
2. Define two initial tables: Videos and Comments.

#### b. Load Data into Snowflake
1. Use Python and the Snowflake connector to load the extracted YouTube data into the Videos and Comments tables in Snowflake.

### 3. Data Transformation and Processing

#### a. Set up dbt (Data Build Tool)
1. Create a dbt project and configure the connection to your Snowflake data warehouse.
2. Define models to preprocess and transform the data.

#### b. Data Transformation
1. Create a table for users who comment on videos.
2. Use dbt models to clean and structure the data appropriately.

#### c. Sentiment Analysis
1. Employ sentiment analysis models such as Vader or TextBlob to estimate the sentiment score of each comment.
2. Add sentiment scores to the comments table.

### 4. Data Visualization

#### a. Set up Tableau or Power BI
1. Connect Tableau or Power BI to your Snowflake data warehouse.
2. Create an interactive dashboard with the following features:
   - **Bar Chart**: Number of comments and videos by month.
   - **Distribution Plot**: Distribution of sentiment scores of comments and average scores of videos.
   - **List**: Top highest score videos.
   - **Scatter Plot**: Sentiment Score vs. Number of Comments for each video.
   - **Pie Chart**: Distribution of sentiment categories (positive, negative, neutral).

#### b. Publish the Dashboard
1. Share the interactive dashboard through Tableau Public or Power BI Service.

### 5. Automation with Airflow

#### a. Set up Apache Airflow
1. Install and configure Apache Airflow.
2. Create DAGs (Directed Acyclic Graphs) to automate the ETL pipeline, from data extraction to loading and transformation.

#### b. Schedule and Monitor Workflows
1. Schedule the workflows to run at specified intervals.
2. Monitor the pipeline to ensure data is updated and processed correctly.

## Conclusion
By following this plan, we will be able to analyze sentiments in YouTube comments from Joma Tech's channel, providing valuable insights through an interactive dashboard. This project will demonstrate the integration of various data engineering and analysis tools, including YouTube API, Snowflake, dbt, sentiment analysis models, Tableau, and Airflow.
