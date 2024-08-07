from fastapi import FastAPI
from src.routes.chatbot import chatbot

app = FastAPI()
app.include_router(chatbot)


@app.get("/root")
def root():
    return {'message': 'API is up!!'}
