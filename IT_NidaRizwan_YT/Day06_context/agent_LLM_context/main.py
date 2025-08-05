
from dotenv import load_dotenv
import os
import asyncio
from agents import (
    Agent, 
    Runner, 
    OpenAIChatCompletionsModel, 
    set_tracing_disabled, 
    RunConfig
)
from openai import AsyncOpenAI

load_dotenv()
set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# External Client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

async def main():
    # Basic Agent with custom system prompt
    agent = Agent(
        name="Assistant",
        instructions="You are talking to user named Osama bin Adnan, be polite and greet him by name",
    )

    result = await Runner.run(
        agent,
        input="Greet me",
        run_config=config,
    )

    print("Agent Running")
    print(f"Result: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())