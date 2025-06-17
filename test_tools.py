import asyncio
from base_agent import Runner
from agent_core import alverri

async def test_tools():
    # Test random_joke tool invocation via the agent
    messages = [
        {"role": "user", "content": "Tell me a joke."}
    ]

    result = await Runner.run(alverri, messages)
    print("Agent reply:", result.final_output)

    # Test encourage tool explicitly
    encourage_message = [
        {"role": "user", "content": "Encourage me with my name Albert."}
    ]
    result2 = await Runner.run(alverri, encourage_message)
    print("Encourage reply:", result2.final_output)

asyncio.run(test_tools())
