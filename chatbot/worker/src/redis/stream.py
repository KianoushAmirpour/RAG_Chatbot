from typing import List


class StreamConsumer:
    def __init__(self, client) -> None:
        self.client = client

    def consume_stream(self, stream_channel: str, count: int) -> List:
        response = self.client.xread(
            streams={stream_channel: '0-0'}, count=count, block=3600000)
        return response

    def delete_message(self, stream_channel, message_id):
        self.client.xdel(stream_channel, message_id)
