from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware to prevent OPTIONS error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Message schemas
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# Load and transform training data
qa_pairs = []

with open("alverri_training_data.json", "r", encoding="utf-8") as f:
    training_data = json.load(f)

    for item in training_data:
        user_msg = next((m for m in item["messages"] if m["role"] == "user"), None)
        assistant_msg = next((m for m in item["messages"] if m["role"] == "assistant"), None)
        if user_msg and assistant_msg:
            qa_pairs.append({
                "keyword": user_msg["content"].lower().strip(),
                "response": assistant_msg["content"]
            })

# Reply generator
def generate_alverri_reply(messages: List[Message]) -> str:
    user_input = messages[-1].content.lower().strip()

    for qa in qa_pairs:
        if qa["keyword"] == user_input:
            return qa["response"]

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
