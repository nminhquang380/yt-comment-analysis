WITH comment_scores AS (
    SELECT
        VIDEO_ID,
        AVG(SCORE) AS AVERAGE_SCORE,
        MAX(SCORE) AS MAX_SCORE,
        MIN(SCORE) AS MIN_SCORE
    FROM
        youtube_sentiment.comments -- This refers to the comments table in dbt
    GROUP BY
        VIDEO_ID
)

SELECT
    v.ID,
    v.TITLE,
    v.DESCRIPTION,
    v.PUBLISHED_AT,
    v.CATEGORY_ID,
    v.DURATION,
    v.CAPTION,
    v.LIKE_COUNT,
    v.COMMENT_COUNT,
    v.VIEW_COUNT,
    cs.AVERAGE_SCORE,
    cs.MAX_SCORE,
    cs.MIN_SCORE
FROM
    youtube_sentiment.videos v -- This refers to the videos table in dbt
LEFT JOIN
    comment_scores cs
ON
    v.ID = cs.VIDEO_ID
