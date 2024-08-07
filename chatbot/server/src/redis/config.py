import redis
from typing import Optional


class Redis:
    def __init__(self) -> None:
        self.connection = None

    def create_connection(self) -> Optional[redis.Redis]:
        try:
            self.connection = redis.Redis(host='localhost', port=6379)
            return self.connection
        except Exception as e:
            print(f"Error for connecting to Redis due to: {e}")
            return None
