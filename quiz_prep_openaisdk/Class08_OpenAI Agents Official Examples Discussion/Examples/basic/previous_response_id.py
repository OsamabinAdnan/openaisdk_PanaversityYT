import random
from dotenv import load_dotenv
import os
from agents import Agent, Runner, AgentHooks, RunContextWrapper, Tool, function_tool, OpenAIChatCompletionsModel, RunConfig, AgentOutputSchemaBase, AgentOutputSchema
from openai import AsyncOpenAI
from typing import Any, Literal
from pydantic import BaseModel
import asyncio
from rich import print
import base64
from dataclasses import dataclass
import json


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

"""This demonstrates usage of the `previous_response_id` parameter to continue a conversation.
The second run passes the previous response ID to the model, which allows it to continue the
conversation without re-sending the previous messages.

Notes:
1. This only applies to the OpenAI Responses API. Other models will ignore this parameter.
2. Responses are only stored for 30 days as of this writing, so in production you should
store the response ID along with an expiration date; if the response is no longer valid,
you'll need to re-send the previous conversation history.
"""

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. be VERY concise.",
        model=model,
    )

    result = await Runner.run(agent, "What is the largest country in South America?")
    print(result.final_output)
    # Brazil

    result = await Runner.run(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id,
    )
    print(result.final_output)
    # Brasilia

async def main_stream():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. be VERY concise.",
        model=model,
    )

    result = Runner.run_streamed(agent, "What is the largest country in South America?")

    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            print(event.data.delta, end="", flush=True)

    print()

    result = Runner.run_streamed(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id,
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    is_stream = input("Run in stream mode? (y/n): ")
    if is_stream == "y":
        asyncio.run(main_stream())
    else:
        asyncio.run(main())