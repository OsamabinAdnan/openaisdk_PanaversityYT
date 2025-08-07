import os
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled, RunHooks, RunContextWrapper
from pprint import pprint
from dotenv import load_dotenv
import asyncio
from rich import print
from dataclasses import dataclass
from typing import Any

load_dotenv()
    
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_NAME= "gemini-2.0-flash"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")

# Create OpenAI client
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=GEMINI_API_KEY,
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

config = RunConfig(
    model=model,
    tracing_disabled=True
    
)

@dataclass
class CustomHook(RunHooks):
    async def on_agent_start(self, context:RunContextWrapper, agent:Agent) -> None:
        print(f"Agent {agent.name} started")
    
    async def on_agent_end(self, context:RunContextWrapper, agent:Agent, output:Any) -> None:
        print(f"Agent {agent.name} ended with output")
    
start_hook = CustomHook()

async def main():
    agent = Agent(
        name="Helpful Assistant",
        instructions="You are content moderation agent. Watch social media content received and flag queries that need help or answer. We will answer anything about AI?",
        model=model,
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Will Agentic AI Die at end of 2025?",
        hooks=start_hook,
        run_config=config,
    )

    print(f"Agent {agent.name} is running")
    pprint(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())