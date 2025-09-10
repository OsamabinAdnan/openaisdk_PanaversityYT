import asyncio
import os
import random
from typing import List
from dotenv import load_dotenv
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled,
    enable_verbose_stdout_logging
    )
from openai import AsyncOpenAI
from pydantic import BaseModel
from rich import print
from typing import Any


load_dotenv()
# set_tracing_disabled(disabled=True)
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

model1 = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=my_client,
)

python_agent = Agent(
    name="Python Agent",
    instructions="You are python expert agent, specially in OOP programming.",
    model=model,
)

# ||||||||||||||||||||||||| Main Agent |||||||||||||||||||||||||

python_agent_clone = python_agent.clone(
    model=model1,
    instructions="You are FastAPI expert agent, specialize in all types of APIs."
)


async def main():
    result = await Runner.run(
        python_agent_clone,
        input=f"What is OOPs, explain in 3 to 5 lines.",
    )
    print(f"\nResult: {result.final_output}\n")
    print(python_agent_clone.instructions)
    print("\nDone!\n")

if __name__ == "__main__":
    asyncio.run(main())

