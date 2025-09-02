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

# @function_tool(
#         strict_mode=False
# )
# def get_weather(city: str) -> str:
#     """
#     Get the weather for a given city

#     Args:
#         city (str): The city to get the weather for

#     Returns:
#         str: The weather for the given city
#     """
#     try:
#         result = requests.get(
#             f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
#         )

#         data = result.json()

#         return f"The current weather in {city} is {data["current"]["temp_c"]} C with {data["current"]["condition"]["text"]}."
    
#     except Exception as e :
#         return f"Could not fetch weather data due to {e}"


@function_tool(
        strict_mode=True,
        name_override="Addition_function",
        description_override="This function will calculate the sum of two numbers.",
        docstring_style="google",
        use_docstring_info=True,
        is_enabled=True
)
def add_two_numbers(a: int, b: int) -> str:
    
    """Add two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
        
    Returns:
        str: The sum of the two numbers.
    """
    result = a + b
    return f"The sum of {a} and {b} is {result}"
        


agent = Agent(
    name="Assitant",
    instructions="You are a helpful assistant. Give complete answer of user query.",
    model=model,
    tools=[add_two_numbers],
)

result = Runner.run_sync(
    agent,
    "What is the sum of 25 and 45?",
    run_config=run_config,
)

print(f"\n{result.final_output}\n")
