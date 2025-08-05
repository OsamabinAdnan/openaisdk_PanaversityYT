
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

python_agent = Agent(
    name="Python Agent",
    instructions="You are expert in Python programming language",
)

typeScript_agent = Agent(
    name="TypeScript Agent",
    instructions="You are expert in TypeScript programming language",
)

nextjs_agent = Agent(
    name="NextJS Agent",
    instructions="You are expert in NextJS framework",
)

main_agent = Agent(
    name="Main Agent",
    instructions="You are the main agent who handoffs tasks to other agents depend on the task given to you by user.",
    handoffs=[
        python_agent,
        typeScript_agent,
        nextjs_agent,
    ]
)

result = Runner.run_sync(
    starting_agent=main_agent,
    input="Create a profile app for me using NextJS framework. ",
    run_config=config,
)

print(result.final_output)