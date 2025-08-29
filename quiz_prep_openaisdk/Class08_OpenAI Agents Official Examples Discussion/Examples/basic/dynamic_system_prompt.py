import random
from dotenv import load_dotenv
import os
from agents import Agent, Runner, AgentHooks, RunContextWrapper, Tool, function_tool, OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI
from typing import Any, Literal
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

class CustomContext:
    def __init__(self, style: Literal["haiku", "pirate", "robot"]):
        self.style = style

def custom_instructions(run_context: RunContextWrapper[CustomContext], agent: Agent[CustomContext]) -> str:
    context = run_context.context
    if context.style == "haiku":
        return "Respond in the style of a haiku only."
    elif context.style == "pirate":
        return "Respond in the style of a pirate only."
    else:
        return "Respond as a robot and say 'beep boop' a lot."

agent = Agent(
    name= "Chat Agent",
    instructions=custom_instructions,
    model=model,
)

async def main():
    choice: Literal["haiku", "pirate", "robot"] = random.choice(["haiku", "pirate", "robot"])
    context = CustomContext(style=choice)
    print(f"### Selected style: {choice}\n")

    user_input = "Tell me a joke"
    
    print(f"### User input: {user_input}\n")
    
    result = await Runner.run(
        agent,
        input=user_input,
        context=context,
    )

    print(f"\n### Assitant: {result.final_output}\n")

if __name__ == "__main__":
    asyncio.run(main())