import asyncio
import os
from typing import Any
from dotenv import load_dotenv
from agents import Agent, RunContextWrapper, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, handoff
from openai import AsyncOpenAI
from agents.run import AgentRunner, set_default_agent_runner, Runner
from agents.extensions import handoff_filters
from rich import print
from pydantic import BaseModel



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

class CustomAgentRunner(AgentRunner):
    async def run (self, starting_agent:Agent, input:str, **kwargs):
        # Custom Preprocessing
        print(f"CustomAgentRunner.run()")
        # input = await self.preprocess(input)

        # Call parent with custom logic
        result = await super().run(starting_agent, input, **kwargs)

        # Custom Postprocessing and analytics
        # await self.log_analytics(result)
        return result

set_default_agent_runner(CustomAgentRunner())

async def main():
    # This agent will used the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=llm_model,
    )

    result = await Runner.run(
        starting_agent=agent, 
        input="hi, how are you?"
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
