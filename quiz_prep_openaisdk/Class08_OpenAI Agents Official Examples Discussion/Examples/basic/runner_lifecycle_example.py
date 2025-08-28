import random
from dotenv import load_dotenv
import os
from agents import Agent, Runner, RunHooks, AgentHooks, RunContextWrapper, Tool, function_tool, OpenAIChatCompletionsModel, RunConfig, Usage
from openai import AsyncOpenAI
from typing import Any
from pydantic import BaseModel
import asyncio
from rich import print


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

class ExampleHooks(RunHooks):
    def __init__(self):
        self.event_counter = 0
    
    def _usage_to_str(self, usage:Usage) -> str:
        return f"{usage.requests} requests, {usage.input_tokens} input tokens, {usage.output_tokens} output tokens, {usage.total_tokens} total tokens"
    
    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Agent {agent.name} started. ==> Usage: {self._usage_to_str(context.usage)}"
        )
    
    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Agent {agent.name} ended with output {output}. ==> Usage: {self._usage_to_str(context.usage)}"
        )
    
    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Tool {tool.name} started. ==> Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_tool_end(
        self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
    ) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Tool {tool.name} ended with result {result}. ==> Usage: {self._usage_to_str(context.usage)}"
        )

    async def on_handoff(
        self, context: RunContextWrapper, from_agent: Agent, to_agent: Agent
    ) -> None:
        self.event_counter += 1
        print(
            f"### {self.event_counter}: Handoff from {from_agent.name} to {to_agent.name}. ==> Usage: {self._usage_to_str(context.usage)}"
        )

hooks = ExampleHooks()

@function_tool
def random_number(max: int) -> int:
    """Generate a random number from 0 to max (inclusive)."""
    random_number = random.randint(0, max)
    return random_number



@function_tool
def multiply_by_two(x: int) -> int:
    """Return x times two."""
    return x * 2


class FinalResult(BaseModel):
    number: int

multiply_agent = Agent(
    name="'Multiply_Agent'",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    # output_type=FinalResult,
    model=model,
)

start_agent = Agent(
    name="'Start_Agent'",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multiplier agent in order to multiply random generated number by multiply agent instructions.",
    tools=[random_number],
    # output_type=FinalResult,
    handoffs=[multiply_agent],
    model=model,
)

async def main() -> None:
    user_input = input("Enter a max number: ")
    try:
        max_number = int(user_input)
        await Runner.run(
            start_agent,
            hooks=hooks,
            input=f"Generate a random number between 0 and {max_number}.",
        )

    except ValueError:
        print("Please enter a valid integer.")
        return

    print("\nDone! Process completed.\n")


if __name__ == "__main__":
    asyncio.run(main())

