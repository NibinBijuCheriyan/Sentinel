import pandas as pd
from datetime import datetime
from .base import BaseIngestor

class TwitterMockIngestor(BaseIngestor):
    def fetch_posts(self, handle: str, limit: int = 100) -> pd.DataFrame:
        """
        Simulates fetching tweets by returning hardcoded sample data.
        In a real scenario, this would load from a CSV or call an API.
        """
        # Mock data for demonstration
        data = [
            {
                "source": "Twitter",
                "handle": handle,
                "date": datetime.now(),
                "content": "I love working at this company! #team",
                "url": f"https://twitter.com/{handle}/status/1"
            },
            {
                "source": "Twitter",
                "handle": handle,
                "date": datetime.now(),
                "content": "This place is a joke. Management has no idea what they are doing.",
                "url": f"https://twitter.com/{handle}/status/2"
            },
            {
                "source": "Twitter",
                "handle": handle,
                "date": datetime.now(),
                "content": "Just saw a great movie last night.",
                "url": f"https://twitter.com/{handle}/status/3"
            },
            {
                "source": "Twitter",
                "handle": handle,
                "date": datetime.now(),
                "content": "I hate everyone who disagrees with me. They should all be fired.",
                "url": f"https://twitter.com/{handle}/status/4"
            }
        ]
        
        return pd.DataFrame(data)
