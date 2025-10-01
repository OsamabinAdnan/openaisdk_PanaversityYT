from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, FunctionTool
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

base_url = os.getenv("BASE_URL")
if not base_url:
    raise ValueError("BASE_URL is not set in environment variables")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client = external_client
)

# Param json schema got from .venv\Lib\site-packages\agents\strict_schema.py
My_SCHEMA = {
    "additionalProperties": False,
    "type": "object",
    "properties": {
        "city": {
            "type":"string"
        }
    },
    "required": [], # city property will show as required in required list | if you dont want it to be required, set strict_json_schema function to False in FunctionTool class
}

# on invoke tool function, which run tool and return result
async def weather(ctx, city: str):
    return f"The current weather in {city} is sunny"

# making tool from FunctionTool class
my_tool = FunctionTool(
    name="get_weather",
    description="Get the current weather for a given location.",
    params_json_schema=My_SCHEMA,
    on_invoke_tool=weather,
    strict_json_schema=False # set to False if you dont want city property to be required | default is True
)

# Create an AI agent with basic instructions
agent: Agent = Agent(
    name="Assistant",
    instructions="You are a helpful weather assistant, entertain user queries politely.",
    model=model,
    tools=[my_tool],
)

# Run the agent synchronously with a test question
result = Runner.run_sync(
    agent,
    "Hello, What is the weather in New York?",
)

print("\nCALLING AGENT")
print("=" * 50)

print(result.final_output)