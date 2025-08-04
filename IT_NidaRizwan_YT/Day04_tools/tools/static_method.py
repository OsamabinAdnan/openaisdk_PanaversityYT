import os
import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("Missing GEMINI_API_KEY environment variable")

MODEL = "gemini-2.0-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

@function_tool
def get_weather(city:str) -> str:
    """Get the weather in a city"""
    print(f"Calling Tool: get_weather({city})")
    return f"The weather in {city} is sunny"

async def main():
    agent = Agent(
        name="Weather Agent",
        instructions="""
        You are a weather agent that will answer questions about the live weather.
        """,
        model=model,
        tools=[get_weather],
    )

    result = await Runner.run(
        agent,
        input="What is the weather in Karachi now?",
        run_config=config,
    )

    print("\nCalling Agent\n")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())