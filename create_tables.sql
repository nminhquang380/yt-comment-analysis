-- Create the videos table
CREATE OR REPLACE TABLE youtube_sentiment.videos (
    ID STRING,
    TITLE STRING,
    DESCRIPTION STRING,
    PUBLISHED_AT TIMESTAMP,
    CATEGORY_ID STRING,
    DURATION INT64,
    CAPTION BOOLEAN,
    LIKE_COUNT INT64,
    COMMENT_COUNT INT64,
    VIEW_COUNT INT64
);

-- Create the comments table
CREATE OR REPLACE TABLE youtube_sentiment.comments (
    REPLY_COUNT INT64,
    AUTHOR STRING,
    TEXT STRING,
    LIKE_COUNT INT64,
    PUBLISHED_AT TIMESTAMP,
    VIDEO_ID STRING,
    SCORE FLOAT64
);

-- -- Create the users table
-- CREATE OR REPLACE TABLE youtube_sentiment.users (
--     AUTHOR STRING,
--     COMMENT_COUNT INT64
-- );
