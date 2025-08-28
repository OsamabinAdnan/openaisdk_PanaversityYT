import random
from dotenv import load_dotenv
import os
from agents import Agent, Runner, AgentHooks, RunContextWrapper, Tool, function_tool, OpenAIChatCompletionsModel, RunConfig
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

# Creating custom AgentHooks

class CustomAgentHooks(AgentHooks):
    def __init__(self, display_name:str):
        self.event_counter = 0
        self.display_name = display_name
    

    async def on_start(self, context:RunContextWrapper, agent:Agent) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started.")
    
    async def on_end(self, context:RunContextWrapper, agent:Agent, output:Any) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended with output {output}")
    
    async def on_handoff(self, context:RunContextWrapper, agent:Agent, source:Agent) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} handed off from {source.name}")
    
    async def on_tool_start(self, context:RunContextWrapper, agent:Agent, tool:Tool) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}")
    
    async def on_tool_end(self, context:RunContextWrapper, agent:Agent, tool:Tool, result:str) -> None:
        self.event_counter += 1
        print(f"### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with result {result}")

@function_tool
def random_number(max: int) -> int:
    """
    Generate a random number from 0 to max (inclusive).
    """
    return random.randint(0, max)


@function_tool
def multiply_by_two(x: int) -> int:
    """Simple multiplication by two."""
    return x * 2

class FinalResult(BaseModel):
    number: int

multiply_agent = Agent(
    name="Multiply_Agent",
    instructions= "Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    # output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Multiply_Agent"), # You can write different hooks name compare to agent name
)

starting_agent = Agent(
    name="Starting_Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multiply agent.",
    tools=[random_number],
    # output_type=FinalResult,
    handoffs=[multiply_agent],
    hooks=CustomAgentHooks(display_name="Starting_Agent"), # You can write different hooks name compare to agent name
)

async def main() -> None:
    user_input = input("Enter the maximum value for random number generation: ")
    try:
        max_number = int(user_input)
        await Runner.run(
            starting_agent,
            input=f"Generate a random number between 0 and {max_number}.",
            run_config=my_runconfig,
        )
    except ValueError:
        print("Please enter a valid integer.")
        return
    
    print("Done!. Process completed.")

if __name__ == "__main__":
    asyncio.run(main())