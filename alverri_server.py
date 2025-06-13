from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import os

app = FastAPI()

# Message schemas
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# Load training data
with open("training_data.json", "r", encoding="utf-8") as f:
    training_data = json.load(f)

# Reply generator
def generate_alverri_reply(messages: List[Message]) -> str:
    user_input = messages[-1].content.lower().strip()

    for item in training_data:
        if item["keyword"] in user_input:
            return item["response"]

    # Default fallback
    return f"Alverri here 🌟 — You said: '{messages[-1].content}'. I’m still learning this topic. Want to teach me?"

# API endpoint
@app.post("/api/chat")
async def chat(req: ChatRequest):
    reply = generate_alverri_reply(req.messages)
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": reply
            }
        }]
    }
