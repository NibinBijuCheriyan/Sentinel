from abc import ABC, abstractmethod
import pandas as pd

class BaseIngestor(ABC):
    @abstractmethod
    def fetch_posts(self, handle: str, limit: int = 100) -> pd.DataFrame:
        """
        Fetches posts for a given handle.
        Returns a DataFrame with columns: ['source', 'handle', 'date', 'content', 'url']
        """
        pass
