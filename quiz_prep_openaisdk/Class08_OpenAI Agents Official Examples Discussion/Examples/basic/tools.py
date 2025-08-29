import random
from dotenv import load_dotenv
import os
from agents import Agent, Runner, AgentHooks, RunContextWrapper, Tool, function_tool, OpenAIChatCompletionsModel, RunConfig, AgentOutputSchemaBase, AgentOutputSchema, GenerateDynamicPromptData, ItemHelpers
from openai import AsyncOpenAI
from typing import Any, Literal
from pydantic import BaseModel
import asyncio
from rich import print
import base64
from dataclasses import dataclass
import json
import argparse


load_dotenv()  # Load environment variables from .env file

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

my_runconfig = RunConfig(
    model=model,
)

class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str


@function_tool
def get_weather(city: str) -> Weather:
    """Get the current weather information for a specified city."""
    print("[debug] get_weather called")
    return Weather(city=city, temperature_range="14-20C", conditions="Sunny with wind.")


agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
    model=model,
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())