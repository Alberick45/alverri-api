# base_agent.py
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

class Agent:
    def __init__(self, name, instructions, tools=None, model="gpt-4o", openai_api_key=None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.model = model
        self.client = AsyncOpenAI(api_key=openai_api_key or os.getenv("OPENAI_API_KEY"))

    async def reply(self, message: str):
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.instructions},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error reaching OpenAI: {e}"

class Runner:
    @staticmethod
    async def run(agent, message_list):
        class Result:
            def __init__(self, reply):
                self.final_output = reply

        reply = await agent.client.chat.completions.create(
            model=agent.model,
            messages=[{"role": "system", "content": agent.instructions}] + message_list
        )
        return Result(reply.choices[0].message.content)
