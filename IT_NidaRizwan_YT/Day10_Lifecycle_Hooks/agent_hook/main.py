import os
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled, RunContextWrapper, AgentHooks
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
class TestAgentHook(AgentHooks):
    def __init__(self, ag_display_name):
        self.event_counter = 0
        self.ag_display_name = ag_display_name
    
    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### {self.ag_display_name} {self.event_counter}: Agent {agent.name} started. Usage: {context.usage}")
    
    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(f"### {self.ag_display_name} {self.event_counter}: Agent {agent.name} ended. Usage: {context.usage}, Output: {output}")

start_agent = Agent(
    name="Content Moderator Agent",
    instructions="You are content moderation agent. Watch social media content received and flag queries that need help or answer. We will answer anything about AI?",
    hooks=TestAgentHook(ag_display_name="content_moderator"),
    model=model
)

async def main():
  result = await Runner.run(
      start_agent,
      input=f"Will Agentic AI Die at end of 2025?.",
      run_config=config,
  )

  print(result.final_output)

asyncio.run(main())
print("--end--")