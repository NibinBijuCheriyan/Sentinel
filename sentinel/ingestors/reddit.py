import praw
import pandas as pd
from datetime import datetime
from .base import BaseIngestor

class RedditIngestor(BaseIngestor):
    def __init__(self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    def fetch_posts(self, handle: str, limit: int = 100) -> pd.DataFrame:
        """
        Fetches recent comments and submissions for a Reddit user.
        handle: Reddit username (without u/)
        """
        try:
            user = self.reddit.redditor(handle)
            posts = []
            
            # Fetch comments
            for comment in user.comments.new(limit=limit):
                posts.append({
                    "source": "Reddit",
                    "handle": handle,
                    "date": datetime.fromtimestamp(comment.created_utc),
                    "content": comment.body,
                    "url": f"https://www.reddit.com{comment.permalink}"
                })
                
            # Fetch submissions
            for submission in user.submissions.new(limit=limit):
                posts.append({
                    "source": "Reddit",
                    "handle": handle,
                    "date": datetime.fromtimestamp(submission.created_utc),
                    "content": f"{submission.title}\n{submission.selftext}",
                    "url": f"https://www.reddit.com{submission.permalink}"
                })
                
            return pd.DataFrame(posts)
        except Exception as e:
            print(f"Error fetching Reddit data: {e}")
            return pd.DataFrame(columns=['source', 'handle', 'date', 'content', 'url'])
