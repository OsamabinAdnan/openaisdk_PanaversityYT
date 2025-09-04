from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, Tool, RunContextWrapper
from openai import AsyncOpenAI
from openai.types.shared import Reasoning
from dotenv import load_dotenv
import os
from rich import print
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any

load_dotenv()

# set_tracing_disabled(True)
enable_verbose_stdout_logging()

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

# Function for failure error function

def default_tool_error_function(ctx: RunContextWrapper[Any], error: Exception) -> str:
    """The default tool error function, which just returns a generic error message."""
    print("Default tool error function called with error")
    return f"An error occurred while running the tool. Please try again. Error: {str(error)}"


@function_tool(failure_error_function=default_tool_error_function)
def user_id (user_id: str) -> str:
    if user_id == "admin123":
        return f"User ID: {user_id}, Access granted"
    else:
        raise ValueError (f"User ID: {user_id}, Access denied")


agent = Agent(
    name="Assitant",
    instructions="You are a helpful assistant. Give complete answer of user query.",
    model=model,
    tools=[user_id],
)

result = Runner.run_sync(
    agent,
    "My id is admin123",
    run_config=run_config,
)

print(f"\n{result.final_output}\n")
