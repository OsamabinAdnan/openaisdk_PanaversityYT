import asyncio
import os
import random
from typing import List
from dotenv import load_dotenv
from agents import (
    Agent, CodeInterpreterTool, Prompt, RunContextWrapper, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled,
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

# @@@@@@@@@@@@@@@@@@ Tools @@@@@@@@@@@@@@@@@@
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@function_tool(is_enabled=False)
def get_time() -> str:
    """Gets the current time."""
    from datetime import datetime
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

code_interpreter_tool = CodeInterpreterTool(
    {
        "container": {
            "type": "auto"
        },
        "type":"code_interpreter"
    }
)

tool_agent = Agent(
    name="Tool_Agent",
    instructions="I have math and time tools.",
    tools=[add_numbers, get_time, code_interpreter_tool],
    model=model,
)

# Check all tools available
async def get_all_tools ():
    context:RunContextWrapper = {}
    all_tools = await tool_agent.get_all_tools(context)

    print(f"Total tools: {len(all_tools)}")
    for tool in all_tools:
        print(f"- {tool.name}")
    print(f"\nTotal detail: {all_tools}")
asyncio.run(get_all_tools())