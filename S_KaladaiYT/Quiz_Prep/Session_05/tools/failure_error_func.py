from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, Tool, RunContextWrapper
from openai import AsyncOpenAI
from openai.types.shared import Reasoning
from dotenv import load_dotenv
import os
from rich import print
from dataclasses import dataclass
from pydantic import BaseModel
import requests

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



@function_tool
def fetch_data():
    return { "name": "Osama", "age": 24 }

def check_is_admin():
    return False

def error_handler(context: RunContextWrapper, error: Exception):
    # Send mail or msg on whatsapp
    print("email sent")
    return "Error handeled"

@function_tool(
    failure_error_function=error_handler
)
def save_data():
    """this function is saving data"""
    raise Exception("Error saving data")
    return "Saved data"
        


agent = Agent(
    name="Assitant",
    instructions="You are a helpful assistant. Give complete answer of user query.",
    model=model,
    tools=[fetch_data, save_data],
)

result = Runner.run_sync(
    agent,
    "Save my name is the database: my name is Osama",
    run_config=run_config,
)

print(f"\n{result.final_output}\n")
