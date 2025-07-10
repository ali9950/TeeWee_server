# main.py
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()

# السماح بالوصول من أي مصدر
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

messages = []
message_id = 1

class SendMessage(BaseModel):
    sender: str
    to: str
    message: str

class Message(BaseModel):
    id: int
    sender: str
    to: str
    message: str

@app.post("/send")
def send_message(data: SendMessage):
    global message_id
    msg = {
        "id": message_id,
        "sender": data.sender,
        "to": data.to,
        "message": data.message
    }
    messages.append(msg)
    message_id += 1
    return {"status": "Message sent ✅", "id": msg["id"]}

@app.get("/messages", response_model=List[Message])
def get_messages(to: str):
    user_messages = [msg for msg in messages if msg["to"] == to]
    return sorted(user_messages, key=lambda x: x["id"])

@app.api_route("/", methods=["GET", "HEAD"])
def home(request: Request):
    if request.method == "HEAD":
        return JSONResponse(content=None, status_code=200)
    return {"message": "Welcome to TeeWee Server 🎉"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
