import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, RunConfig, function_tool
from openai import AsyncOpenAI
import agentops
import requests
import asyncio

load_dotenv()
set_tracing_disabled(True)

AGENT_OPS_API = os.getenv("AGENT_OPS_AI_API")
if not AGENT_OPS_API:
    raise ValueError("Agent ops API not found in env file")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI API not found in env file")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

test = agentops.init(AGENT_OPS_API)

@function_tool
def get_weather(city:str) -> str :
    """ Get the current weather for a given city."""
    result = requests.get("http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
    data = result.json()
    return f"The current weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are helpful Assistent. Call get_weather tool to get latest weather for a city.",
        model=model,
        tools=[get_weather],
        tool_use_behavior="run_llm_again"
    )

    result = await Runner.run(agent, "what is the weather in lahore", run_config=config)
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":
    asyncio.run(main())