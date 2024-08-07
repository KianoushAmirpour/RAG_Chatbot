from typing import Dict, Optional


class Producer:
    def __init__(self, client) -> None:
        self.client = client

    def add_to_stream(self, data: Dict[str, str], stream_channel: str) -> Optional[str]:
        try:
            msg_id = self.client.xadd(name=stream_channel, id='*', fields=data)
            print(f"Message id {msg_id} added to `{stream_channel}` stream.")
            return msg_id
        except Exception as e:
            print(f"Error adding message to stream: {e}")
            return None
