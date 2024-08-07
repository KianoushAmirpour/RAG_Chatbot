import redis
from typing import Optional


class Redis:
    def __init__(self) -> None:
        pass

    def create_connection(self) -> Optional[redis.Redis]:
        try:
            self.connection = redis.Redis(host='localhost', port=6379)
            return self.connection
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            return None
