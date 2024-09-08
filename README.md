# **Sentiment Analysis on YouTube Comments**

## **Introduction**
This project performs sentiment analysis on YouTube comments from the **Max Yoko** channel, a German content creator discussing higher education in Germany. As I am personally interested in this topic, the project aims to build an automated data pipeline that extracts, processes, and visualizes insights from the comments. The final result will be an interactive dashboard using **Looker Studio**, providing insights into viewer sentiments toward the channel's videos.

The pipeline integrates several tools:
- [**YouTube API**](https://developers.google.com/youtube/v3) for data extraction.
- [**BigQuery**](https://cloud.google.com/bigquery?hl=en) as the data warehouse.
- [**dbt**](https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup) for data transformation.
- **Sentiment Analysis** using [**TextBlob**](https://textblob.readthedocs.io/en/dev/quickstart.html) model.
- [**Looker Studio**](https://lookerstudio.google.com/) for visualization.
- [**GCP Composer**](https://cloud.google.com/composer/docs/concepts/overview) to automate the workflow.

Here is the [Final Dashboard](https://github.com/nminhquang380/yt-comment-analysis) in **Looker Studio**.
## **Project Plan**

### **1. Data Extraction**

#### a. Set up YouTube Data API
1. **Create a project** in the Google Developer Console.
2. Enable the **YouTube Data API v3**.
3. **Generate API credentials** (API key) for authentication. Store these securely as they are required for API calls.

#### b. Extract Data from YouTube
1. **Use the YouTube API** to gather:
   - Video metadata (title, description, statistics: likes, views, etc.).
   - Comment details (author, comment text, like count, publication date).
2. **Save extracted data** as CSV files for local backup.
   - Keep separate CSV files for `videos` and `comments`.

#### c. Preprocess the Extracted Data
1. **Clean and normalize** the data to handle missing values, duplicates, and standardize formats.
   - Example: Convert `published_at` to a standardized datetime format.
2. **Calculate sentiment scores** using TextBlob for each comment.
   - Add a new column for sentiment score in the `comments` CSV file.
   - Save preprocessed CSVs for future use.

### **2. Data Loading**

#### a. BigQuery Setup
1. **Create a BigQuery dataset**: Configure necessary project and dataset settings in your GCP account.
2. **Create Tables**:
   - `videos`: Holds raw video data (columns: ID, title, description, published_at, like_count, comment_count, view_count, etc.).
   - `comments`: Contains raw comment data (columns: video_id, author, text, like_count, sentiment_score, published_at, etc.).

#### b. Load Data into BigQuery
1. **Use Python** with the BigQuery connector to load the processed data into the `videos` and `comments` tables.
   - You can use the `pandas` library in Python to read CSVs and load data into BigQuery using `google.cloud.bigquery` library functions.

### **3. Data Transformation**

#### a. Set up dbt
1. **Initialize a dbt project** and configure it to connect with your BigQuery dataset.
   - Install dbt and configure the `profiles.yml` file to connect to your BigQuery dataset.
   - Define your models inside `models/` folder.

#### b. Create dbt Models
1. **Create a `users` table**: Use dbt to aggregate commenter data (e.g., number of comments per user).
   - Model file: `models/users.sql`
2. **Create a `video_scores` table**: Calculate the average, max, and min sentiment scores for each video.
   - Model file: `models/video_scores.sql`
3. **Other Transformations**:
   - Clean the `comments` table (e.g., filter out invalid comments, standardize text).
   - Create `staging` models to aggregate and clean data before loading into final models.

### **4. Data Visualization**

#### a. Build the Dashboard
1. **Use Looker Studio** (formerly Google Data Studio) to connect to BigQuery and visualize the processed data.
   - Create connectors to the `videos`, `comments`, and `users` tables in BigQuery.
2. **Create Interactive Visualizations**:
   - **Bar Chart**: Number of videos and comments by month.
   - **Distribution Plot**: Distribution of sentiment scores across comments.
   - **List**: Top videos by highest sentiment scores.
   - **Scatter Plot**: Comment count vs. sentiment score per video.
   - **Pie Chart**: Sentiment categories (positive, neutral, negative).

#### b. Publish the Dashboard
1. **Share** the interactive dashboard through Looker Studio's sharing features.

### **5. Automation with GCP Composer**

#### a. Set up GCP Composer
1. **Create an environment** in GCP Composer to orchestrate the workflow with Apache Airflow.
2. **Install dependencies** in Composer (e.g., `google-cloud-bigquery`, `pandas`).
3. **Configure the DAG**: Define tasks to automate data extraction, loading, transformation, and dashboard update in Airflow.
   - Upload Python scripts and Airflow DAGs to run the ETL pipeline, dbt transformations, and Looker Studio updates.

#### b. Schedule and Monitor Workflows
1. **Set up scheduling**: Use Airflow to schedule the pipeline to run at regular intervals (e.g., daily, weekly).
2. **Monitor Airflow**: Use the Airflow UI to monitor DAG runs and handle any task failures.

## **Conclusion**
This project automates the sentiment analysis of YouTube comments using modern data engineering tools. By integrating the YouTube API, BigQuery, dbt, GCP Composer, and Looker Studio, it delivers real-time insights through an interactive dashboard. This pipeline is scalable and can be adapted for other YouTube channels or use cases.
