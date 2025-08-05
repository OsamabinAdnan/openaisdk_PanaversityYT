from dataclasses import dataclass
from dotenv import load_dotenv
import os
import asyncio
from agents import (
    Agent, 
    Runner, 
    OpenAIChatCompletionsModel, 
    set_tracing_disabled, 
    function_tool, 
    RunContextWrapper,
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

@dataclass
class UserInfo:
    name:str
    age: int
    id:int

@function_tool
async def fetch_info(ctx:RunContextWrapper[UserInfo]) -> str:
    """Fetch the age of the user. Call this function to get user's age information."""
    print("Tool function called")
    return f"The user name is {ctx.context.name}, age is {ctx.context.age} and id is {ctx.context.id}"

async def main():
    user_info = UserInfo("Osama bin Adnan", 36, 1234)

    agent = Agent[UserInfo](
        name="Assistant",
        instructions="You are a helpful assistant.",
        tools=[fetch_info],
    )

    result = await Runner.run(
        agent,
        input="What is the age of the user?",
        run_config=config,
        context=user_info,
    )

    print("Agent Running")
    print(f"Result: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())