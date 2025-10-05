import os
from dotenv import load_dotenv
from agents import Agent, ModelSettings, Runner, function_tool, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, handoff, RunHooks
from openai import AsyncOpenAI
from rich import print
import asyncio

load_dotenv()

# enable_verbose_stdout_logging()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

class CustomRunHooks(RunHooks):
    async def on_agent_start(self, context, agent):
        print("agent start hua ha.", agent.name)


get_weather = Agent(
    name="get_weather",
    instructions="you always respond today karachi weather is cloudy.",
    model=llm_model,
    handoff_description="get the weather for given city",
)


main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    handoffs=[get_weather],
    model=llm_model,
)

result = Runner.run_sync(
    main_agent,
    "what is the current weather in karachi",
    hooks=CustomRunHooks()
)

print(result.final_output)