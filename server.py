from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import json
import re
import os
from fastapi.middleware.cors import CORSMiddleware

from agent_core import alverri
from base_agent import Runner

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class TrainMessage(BaseModel):
    user: str
    assistant: str

# In-memory Q&A pairs loaded from file
qa_pairs = []

try:
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
except FileNotFoundError:
    print("📁 No training data found. Starting fresh.")
    training_data = []

# Main response generator
async def generate_alverri_reply(messages: List[Message]) -> str:
    user_input = messages[-1].content.strip()

    # Pattern to learn new pairs
    if user_input.lower().startswith("alverri, learn this:"):
        try:
            match = re.match(r"Alverri, learn this:\s*'(.*?)'\s*→\s*'(.*?)'", user_input, re.IGNORECASE)
            if match:
                prompt, completion = match.groups()

                new_entry = {
                    "messages": [
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": completion}
                    ]
                }

                try:
                    with open("alverri_training_data.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                except FileNotFoundError:
                    data = []

                data.append(new_entry)

                with open("alverri_training_data.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                qa_pairs.append({
                    "keyword": prompt.lower().strip(),
                    "response": completion
                })

                return f"✅ Learned: ‘{prompt}’ → ‘{completion}’"
            else:
                return "❌ Format error. Use: Alverri, learn this: 'question' → 'answer'"
        except Exception as e:
            return f"⚠️ Learning failed: {str(e)}"

    # Check memory
    for qa in qa_pairs:
        if qa["keyword"] == user_input.lower():
            return qa["response"]

    # Else, fallback to OpenAI agent
    raw_messages = [{"role": m.role, "content": m.content} for m in messages]
    result = await Runner.run(alverri, raw_messages)
    return result.final_output

# Chat endpoint
@app.post("/api/chat")
async def chat(req: ChatRequest):
    reply = await generate_alverri_reply(req.messages)
    return {
        "choices": [{
            "message": {
                "role": "assistant",
                "content": reply
            }
        }]
    }

# Manual training endpoint
@app.post("/api/train")
async def train(new_data: TrainMessage):
    new_pair = {
        "messages": [
            {"role": "user", "content": new_data.user},
            {"role": "assistant", "content": new_data.assistant}
        ]
    }

    try:
        with open("alverri_training_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(new_pair)

    with open("alverri_training_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    qa_pairs.append({
        "keyword": new_data.user.lower().strip(),
        "response": new_data.assistant
    })

    return {"message": "✅ New training data added successfully."}
