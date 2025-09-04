from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, Tool, RunContextWrapper, ModelSettings
from openai import AsyncOpenAI
from openai.types.shared import Reasoning
from dotenv import load_dotenv
import os
from rich import print
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any
from datetime import datetime

load_dotenv()

# set_tracing_disabled(True)
# enable_verbose_stdout_logging()

gemini_api_key=os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set. Please set it in the .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

run_config = RunConfig(
    model=model,
)


@function_tool()
def get_time() -> str:
    try:
        """Get the current time."""
        print("get_time tool called")
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    except Exception as e:
        return f"An error occurred while running the tool. Please try again. Error: {str(e)}"
    
@function_tool()
def multiply_numbers(a: int, b: int) -> str:
    """multiply two numbers.
    Args:
        a: The first number.
        b: The second number.
    Returns:
        The multiplication of the two numbers.
    """
    print("multiply_numbers tool called")
    result = a * b
    return f"The multiplication of {a} and {b} is {result}"


agent = Agent(
    name="Assitant",
    instructions="You are a helpful assistant. Give complete answer of user query.",
    model=model,
    tools=[multiply_numbers, get_time],
    model_settings=ModelSettings(
        tool_choice="auto",
        parallel_tool_calls=False,
    ),
)

result = Runner.run_sync(
    agent,
    "What is current time in Karachi?, What is 25 * 125?",
    # "Hello",
    run_config=run_config,
)

print(f"\n{result.final_output}\n")
