import os
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from dotenv import load_dotenv
from preprocess_data import clean_text

dotenv_path = "/home/micasidad/Desktop/yt-comment-analysis/.env"
load_dotenv(dotenv_path)

API_KEY = os.getenv('YOUTUBE_API_KEY')
# CHANNEL_ID = os.getenv('CHANNEL_ID')
CHANNEL_ID = 'UCc6RN6wpBR3AF0rBwsB5G7g' # Max Yoko

def get_youtube_service():
    return googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

def get_channel_videos(youtube, channel_id):
    request = youtube.search().list(
        part='id',
        channelId=channel_id,
        maxResults=50,
        type='video'
    )
    response = request.execute()

    videos = []
    while request is not None:
        response = request.execute()
        videos += response['items']
        request = youtube.search().list_next(request, response)

    return videos

def get_video_metadata(youtube, video_id):
    request = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    )
    response = request.execute()

    try:
        response = response['items'][0]
        data = {
            'ID': response['id'],
            'TITLE': response['snippet']['title'],
            'DESCRIPTION': clean_text(response['snippet']['description']),
            'PUBLISHED_AT': response['snippet']['publishedAt'],
            'CATEGORY_ID': response['snippet']['categoryId'],
            'DURATION': response['contentDetails']['duration'],
            'CAPTION': response['contentDetails']['caption'],
            'LIKE_COUNT': response['statistics']['likeCount'],
            'COMMENT_COUNT': response['statistics']['commentCount'],
            'VIEW_COUNT': response['statistics']['viewCount'],

        }
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def get_video_comments(youtube, video_id):
    next_page_token = None
    comments = []

    try:
        while True:
            # Fetch comment threads from the YouTube API
            comment_thread = youtube.commentThreads().list(
                part="snippet,replies",
                order="relevance",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
            ).execute()

            # Extract comments from JSON response
            for item in comment_thread['items']:
                snippet = item['snippet']['topLevelComment']['snippet']
                comment = {
                    'REPLY_COUNT': item['snippet']['totalReplyCount'],
                    'AUTHOR': snippet['authorDisplayName'],
                    'TEXT': clean_text(snippet['textDisplay']),
                    'LIKE_COUNT': snippet['likeCount'],
                    'PUBLISHED_AT': snippet['publishedAt'],
                    'VIDEO_ID': video_id,
                }
                comments.append(comment)

                # Extract replies, if any
                if 'replies' in item:
                    for reply_item in item['replies']['comments']:
                        reply_snippet = reply_item['snippet']
                        reply = {
                            'REPLY_COUNT': 0,  # Replies don't have their own replies
                            'AUTHOR': reply_snippet['authorDisplayName'],
                            'TEXT': reply_snippet['textDisplay'],
                            'LIKE_COUNT': reply_snippet['likeCount'],
                            'PUBLISHED_AT': reply_snippet['publishedAt'],
                            'VIDEO_ID': video_id,
                        }
                        comments.append(reply)

            # Handle pagination
            next_page_token = comment_thread.get("nextPageToken")
            if not next_page_token:
                break
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []
        
    return comments

def main():
    youtube = get_youtube_service()

    # Get all videos from the channel
    videos = get_channel_videos(youtube, CHANNEL_ID)
    video_ids = [video['id']['videoId'] for video in videos]

    # Get metadata and comments for each video
    all_videos_data = []
    all_comments_data = []

    for video_id in video_ids:
        video_metadata = get_video_metadata(youtube, video_id)
        if video_metadata:
            all_videos_data.append(video_metadata)

        comments = get_video_comments(youtube, video_id)
        all_comments_data.extend(comments)

    # Save metadata to CSV
    videos_df = pd.DataFrame(all_videos_data)
    videos_df.to_csv('data/unpreprocessed/videos.csv', index=False)

    # Save comments to CSV
    comments_df = pd.DataFrame(all_comments_data)
    comments_df.to_csv('data/unpreprocessed/comments.csv', index=False)

if __name__ == '__main__':
    main()
