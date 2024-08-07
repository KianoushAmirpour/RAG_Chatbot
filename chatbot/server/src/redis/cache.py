from typing import Dict, Union, List
from redis.commands.json.path import Path


class Cache:
    def __init__(self, client) -> None:
        self.client = client

    def get_chat_history(self, token: str) -> Dict[str, Union[str, List]]:
        data = self.client.json().get(str(token), Path.root_path())
        return data
