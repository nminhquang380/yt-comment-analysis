-- models/users.sql

WITH user_data AS (
    SELECT
        AUTHOR,
        COUNT(*) AS COMMENT_COUNT
    FROM
        {{ source('youtube_sentiment', 'comments') }}  -- Referencing the raw_comments table
    GROUP BY
        AUTHOR
)

SELECT * FROM user_data
