from base_agent import Agent
from tools import all_tools
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

alverri = Agent(
    name="Alverri",
    instructions="You are Alverri, a Christian AI who helps Albert with tech, learning, and faith.",
    tools=all_tools,
    model="gpt-4o",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
