import asyncio
import os
import random
from typing import List
from dotenv import load_dotenv
from agents import (
    Agent, Runner, OpenAIChatCompletionsModel, Usage, function_tool, set_tracing_disabled,
    enable_verbose_stdout_logging, AgentHooks, RunContextWrapper, Tool, ModelResponse, RunHooks
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


# ||||||||||||||||||||||||| RunHook |||||||||||||||||||||||||

class My_Runner_Hook(RunHooks):
    def __init__(self):
        self.event_counter = 0
        
    # def _usage_to_str(self, usage:Usage) -> str:
    #     return f"Request: {usage.requests}, Input Tokens: {usage.input_tokens}, Output Tokens: {usage.output_tokens}, Total tokens: {usage.total_tokens}"

    async def on_agent_start(self,context:RunContextWrapper, agent:Agent):
        self.event_counter += 1
        print(f"### Agent Started ### `{self.event_counter}`, Agent: `{agent.name}` started.")
        # Usage: `{self._usage_to_str(context.usage)}`
    
    async def on_agent_end(self,context:RunContextWrapper, agent:Agent, output:Any):
        self.event_counter += 1
        print(f"### Agent Ended ### `{self.event_counter}`: Agent: `{agent.name}` ended.")
    
    async def on_tool_start(self, context:RunContextWrapper, agent:Agent, tool:Tool):
        self.event_counter += 1
        print(f"### Tool Started ### `{self.event_counter}`: Tool: `{tool.name}` started. Agent: `{agent.name}`")
    
    async def on_tool_end(self, context:RunContextWrapper, agent:Agent, tool:Tool, result:str):
        self.event_counter += 1
        print(f"### Tool Ended ### `{self.event_counter}`: Tool: `{tool.name}` ended with {result}. Agent: `{agent.name}`")

    async def on_handoff(self, context:RunContextWrapper, from_agent: Agent, to_agent: Agent):
        self.event_counter += 1
        print(f"### Handoff ### `{self.event_counter}`: Handoff from `{from_agent.name}` to `{to_agent.name}`.")
    
    async def on_llm_start(self, context:RunContextWrapper, agent:Agent, system_prompt, input_items):
        self.event_counter += 1
        print(f"### LLM Started ### `{self.event_counter}`: LLM started for agent: `{agent.name}`.")
    
    async def on_llm_end(self, context:RunContextWrapper, agent:Agent, response:ModelResponse):
        self.event_counter += 1
        print(f"### LLM Ended ### `{self.event_counter}`: LLM ended for agent: `{agent.name}`. Response: `{response.output[0]}`.")



my_runner_hook = My_Runner_Hook()

# ||||||||||||||||||||||||| Handoff Agent |||||||||||||||||||||||||

weather_agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You help customers with their weather questions. By the way, current weather is Karachi is cloudy with 30 C.",
    model=model,
    handoff_description="Ask me any question about the weather",
)

multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    model=model
)

# ||||||||||||||||||||||||| Main Agent |||||||||||||||||||||||||

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multiply agent.",
    tools=[random_number],
    handoffs=[multiply_agent],
    model=model

)


user_input = input("Enter a max number: ")
result =  Runner.run_sync(
    start_agent,
    input=f"Generate a random number between 0 and {user_input}.",
    hooks=my_runner_hook
)
print(f"Result: {result.final_output}")
print("Done!")
    
        