import ast
import uuid
from ..schema.model import Chat
from ..redis.cache import Cache
from ..redis.config import Redis
from ..redis.producer import Producer
from ..redis.stream import StreamConsumer
from ..socket.utils import validate_token
from ..socket.connection import ConnectionManager
from redis.commands.json.path import Path
from fastapi import APIRouter, WebSocket, HTTPException, WebSocketDisconnect, Depends

chatbot = APIRouter()
connection_manager = ConnectionManager()
redis_client = Redis().create_connection()


@chatbot.post('/generate_token')
def generate_token(name: str):
    token = str(uuid.uuid4())
    if name is None or name == "":
        raise HTTPException(status_code=400, detail="Name is not valid.")
    chat_session = Chat(token=token, messages=[], urls=[], name=name)
    redis_client.json().set(str(token), Path.root_path(), chat_session.model_dump())
    redis_client.expire(str(token), 3600)
    return chat_session.model_dump()


@chatbot.get('/get_chat_history')
def get_chat_history(token: str):
    data = Cache(redis_client).get_chat_history(token)
    if data == None:
        raise HTTPException(status_code=400,
                            detail="Session expired or doesn't exist.")
    else:
        return data


@chatbot.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket = WebSocket, token: str = Depends(validate_token)):
    await connection_manager.connect(websocket)
    producer = Producer(redis_client)
    consumer = StreamConsumer(redis_client)
    try:
        while True:
            query = await websocket.receive_text()
            stream_query = {}
            stream_query[token] = query
            producer.add_to_stream(
                data=stream_query, stream_channel='query_channel')
            response = consumer.consume_stream(
                stream_channel='response_channel', count=1)
            for _, messages in response:
                for message in messages:
                    response_token = [k.decode('utf-8')
                                      for k, v in message[1].items()][0]
                    if token == response_token:
                        retrieved_info = [
                            v.decode('utf-8') for k, v in message[1].items()][0]
                        retrieved_info = ast.literal_eval(retrieved_info)
                        await connection_manager.send_message(retrieved_info['msg'], websocket)
                    consumer.delete_message(
                        stream_channel='response_channel', message_id=message[0].decode('utf-8'))
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
