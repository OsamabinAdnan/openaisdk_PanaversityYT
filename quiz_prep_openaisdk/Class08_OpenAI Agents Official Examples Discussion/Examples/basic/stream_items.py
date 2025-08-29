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

@function_tool
def how_many_jokes() -> int:
    """Return a random integer of jokes to tell between 1 and 10 (inclusive)."""
    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
        model=model,
    )

    result = Runner.run_streamed(
        agent,
        input="Hello",
    )
    print("\n=== Run starting ===\n")
    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("\n=== Run complete ===\n")


if __name__ == "__main__":
    asyncio.run(main())