import asyncio
import os
import random
from typing import List
from dotenv import load_dotenv
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled,
    enable_verbose_stdout_logging, AgentHooks, RunContextWrapper, Tool, ModelResponse
    )
from openai import AsyncOpenAI
from pydantic import BaseModel
from rich import print
from typing import Any


load_dotenv()
# set_tracing_disabled(disabled=True)
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)
# ||||||||||||||||||||||||| Tools |||||||||||||||||||||||||
@function_tool
def random_number(max: int) -> int:
    """
    Generate a random number up to the provided maximum.
    """
    random_num = random.randint(0, max)
    print(f"Random number: {random_num}")
    return random_num


@function_tool
def multiply_by_two(x: int) -> int:
    """Simple multiplication by two."""
    return x * 2


# ||||||||||||||||||||||||| AgentHook |||||||||||||||||||||||||

class My_Agent_Hooks(AgentHooks):
    def __init__(self, agent_display_name):
        self.event_counter = 0
        self.agent_display_name = agent_display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent):
        self.event_counter += 1
        print(f"### ==> Starting {self.agent_display_name} at event {self.event_counter} ###")
    
    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any):
        self.event_counter += 1
        print(f"### ==> Ended {self.agent_display_name} at event {self.event_counter} ###")
    
    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent):
        self.event_counter += 1
        print(f"### ==> Handoff to `{agent.name}` from `{source.name}` at event {self.event_counter} ###")

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool):
        self.event_counter += 1
        print(f"### ==> Starting {tool.name} tool from `{agent.name}` at event {self.event_counter} ###")
    
    async def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool: Tool, result:str):
        self.event_counter += 1
        print(f"### ==> Ended {tool.name} tool from `{agent.name}` at event {self.event_counter} ###")

    async def on_llm_start(self, context: RunContextWrapper, agent: Agent, system_prompt, input_items):
        self.event_counter += 1
        print(f"### ==> Starting LLM from `{agent.name}` at event {self.event_counter} ###")
    
    async def on_llm_end(self, context: RunContextWrapper, agent: Agent, response:ModelResponse):
        self.event_counter += 1
        print(f"### ==> Ended LLM from `{agent.name}` at event {self.event_counter} response: {response} ###")
    



# ||||||||||||||||||||||||| Handoff Agent |||||||||||||||||||||||||

weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You help customers with their weather questions. By the way, current weather is Karachi is cloudy with 30 C.",
    model=model,
    handoff_description="Ask me any question about the weather",
    hooks=My_Agent_Hooks("Weather Agent"),
)

multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    hooks=My_Agent_Hooks(agent_display_name="Multiply Agent"),
    model=model
)

# ||||||||||||||||||||||||| Main Agent |||||||||||||||||||||||||

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multiply agent.",
    tools=[random_number],
    handoffs=[multiply_agent],
    hooks=My_Agent_Hooks(agent_display_name="Start Agent"),
    model=model

)


async def main() -> None:
    user_input = input("Enter a max number: ")
    result = await Runner.run(
        start_agent,
        input=f"Generate a random number between 0 and {user_input}.",
    )
    print(f"Result: {result.final_output}")

    print("Done!")

    
        

if __name__ == "__main__":
    asyncio.run(main())

