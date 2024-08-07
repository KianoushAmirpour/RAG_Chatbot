from uuid import uuid4
from typing import List
from datetime import datetime
from pydantic import BaseModel


class QueryResponse(BaseModel):
    id: str = str(uuid4())
    msg: str
    timestamp: str = str(datetime.now())


class Urls(BaseModel):
    id: str = str(uuid4())
    url: str
    timestamp: str = str(datetime.now())
