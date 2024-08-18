import re
from html import unescape
import string
from textblob import TextBlob

'''
TODO:
- Transform DURATION from STRING to INT64
- Transform PUBLISHED_AT from STRING to TIMESTAMP
- Clean TEXT of raw_comments
- Estimate SCORE of comments
- Calculate AVERAGE_SCORE, MAX_SCORE, MIN_SCORE of videos
- Create users table
'''

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Unescape HTML entities (e.g., &amp; to &)
    text = unescape(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Transform DURATION
def iso8601_to_minutes(duration: str) -> int:
    # Use regex to find hours, minutes, and seconds in the duration string
    hours = re.search(r'(\d+)H', duration)
    minutes = re.search(r'(\d+)M', duration)
    seconds = re.search(r'(\d+)S', duration)
    
    # Convert found values to integers, default to 0 if not found
    hours = int(hours.group(1)) if hours else 0
    minutes = int(minutes.group(1)) if minutes else 0
    seconds = int(seconds.group(1)) if seconds else 0
    
    # Calculate total minutes
    total_minutes = hours * 60 + minutes + (seconds / 60)
    
    return int(total_minutes)

def get_sentiment_score(text):
    # Create a TextBlob object
    blob = TextBlob(text)

    # Return the sentiment score
    return blob.sentiment.polarity