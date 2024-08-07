from uuid import uuid4
from typing import List
from datetime import datetime
from pydantic import BaseModel


class Url(BaseModel):
    id: str = str(uuid4())
    url: str
    timestamp: str = str(datetime.now())


class QueryResponse(BaseModel):
    id: str = str(uuid4())
    msg: str
    timestamp: str = str(datetime.now())


class Chat(BaseModel):
    token: str
    messages: List[QueryResponse]
    urls: List[Url]
    name: str
    session_start_time: str = str(datetime.now())
