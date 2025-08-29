import random
from dotenv import load_dotenv
import os
from agents import Agent, Runner, AgentHooks, RunContextWrapper, Tool, function_tool, OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI
from typing import Any, Literal
from pydantic import BaseModel
import asyncio
from rich import print
import base64


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

FILEPATH = os.path.join(os.path.dirname(__file__),"media/image_bison.jpg")

def image_to_base64(image_path):
    with open (image_path, "rb") as image_file:
        encoded_string =base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

async def main():
    # Print base64-encoded image
    b64_image = image_to_base64(FILEPATH)

    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=model,
    )

    result = await Runner.run(
        agent,
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "detail": "auto",
                        "image_url": f"data:image/jpeg;base64,{b64_image}",
                    }
                ],
            },
            {
                "role": "user",
                "content": "What do you see in this image?",
            },
        ],
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())