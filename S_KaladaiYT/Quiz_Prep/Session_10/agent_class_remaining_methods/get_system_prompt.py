import asyncio
import os
import random
from typing import List
from dotenv import load_dotenv
from agents import (
    Agent, Prompt, RunContextWrapper, Runner, OpenAIChatCompletionsModel, set_tracing_disabled,
    enable_verbose_stdout_logging, ModelSettings
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
    instructions="You are an expert Python agent.",
    model=model1,
)

python_tool = python_agent.as_tool(
    tool_name="Python_Tool",
    tool_description="Useful for executing Python code.",
)


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model,
    tools=[python_tool],
    model_settings=ModelSettings(
        tool_choice="required"
    ),
    prompt=Prompt(
        id="pmpt_68a9aebde7a08194a7f6d3f08c0310980db39709860bbc40",
        version="4",
        variables= {
            "topic": "python programming"
        }
    )
)

# Get system prompt (Method)
async def get_system_prompt():
    context:RunContextWrapper = {}
    get_sys_prompt = await agent.get_system_prompt(context)
    print(f"\nGet system prompt: `{get_sys_prompt}`\n")

# Get prompt (Method)
async def get_prompt():
    context:RunContextWrapper = {}
    get_prompt = await agent.get_prompt(context)
    print(f"Get prompt: `{get_prompt}`\n")



# async def main():
#     result = await Runner.run(
#         agent,
#         # "Hello, how are you?",
#         "What is OOPs, explain in 3 to 5 lines",
#     )
#     print(f"\nResult: {result.final_output}\n")
#     print("\nDone!\n")

if __name__ == "__main__":
    asyncio.run(get_system_prompt())
    asyncio.run(get_prompt())


