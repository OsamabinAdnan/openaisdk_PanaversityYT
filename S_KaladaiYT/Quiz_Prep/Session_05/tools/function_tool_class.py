from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, Tool, RunContextWrapper, FunctionTool
from openai import AsyncOpenAI
from openai.types.shared import Reasoning
from dotenv import load_dotenv
import os
from rich import print
from dataclasses import dataclass
from pydantic import BaseModel
import requests
from typing import Any
import json
import asyncio


load_dotenv()

# set_tracing_disabled(True)
enable_verbose_stdout_logging()

gemini_api_key=os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set. Please set it in the .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

run_config = RunConfig(
    model=model,
)

# Schema for params_json_schema
json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "Name of the person"},
    },
    "required": ["name"],
    "additionalProperties": False
}

# tool for on_invoke_tool
async def greet_invoke(ctx: RunContextWrapper[Any], input:str):
    """Ye function tool call per chalay ga"""
    args = json.loads(input) if input else {}
    # print(args)
    name = args.get("name")
    return f"Hello {name}!"

custom_function_tool = FunctionTool(
    name="Greeting_Function_Tool",
    description="Greet user with his/her name",
    params_json_schema=json_schema,
    on_invoke_tool=greet_invoke,
)

agent = Agent(
    name="Assitant",
    instructions="You are a helpful assistant. Give complete answer of user query.",
    model=model,
    tools = [custom_function_tool],
    
)
async def main():
    result = await Runner.run(
        agent,
        "Hi my name is Osama, how are you?",
        run_config=run_config,
    )

    print(f"\n{result.final_output}\n")


if __name__ == "__main__":
    asyncio.run(main())