from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []
message_id = 0

class Message(BaseModel):
    sender: str
    receiver: str
    message: str

@app.post("/send")
async def send_message(sender: str, receiver: str, message: str):
    global message_id
    message_id += 1
    messages.append({
        "id": message_id,
        "sender": sender,
        "receiver": receiver,
        "message": message
    })
    return {"success": True}

@app.get("/messages")
def get_messages(receiver: str, after: int = 0):
    return [msg for msg in messages if msg["receiver"] == receiver and msg["id"] > after]