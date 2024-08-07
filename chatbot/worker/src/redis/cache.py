from typing import Dict, Union, List
from redis.commands.json.path import Path


class Cache:
    def __init__(self, client) -> None:
        self.client = client

    def get_chat_history(self, token: str) -> Dict[str, Union[str, List]]:
        data = self.client.json().get(str(token), Path.root_path())
        return data

    def add_message_to_cache(self, token: str, source: str,  message: Dict):
        if source == 'User':
            message['msg'] = 'User: ' + message['msg']
        elif source == 'Bot':
            message['msg'] = 'Bot: ' + message['msg']
        self.client.json().arrappend(str(token), Path('.messages'), message)

    def add_urls_to_cache(self, token: str, urls: Dict):
        self.client.json().arrappend(str(token), Path('.urls'), urls)
