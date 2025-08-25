from agents import Agent, RunContextWrapper, OpenAIChatCompletionsModel, enable_verbose_stdout_logging
from openai import AsyncOpenAI
import json
from dotenv import load_dotenv
import os
from rich import print


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
    model="gemini-2.0-flash",
    openai_client=external_client,
)

python_agent = Agent(
    name="PythonAgent",
    instructions="You are a Python agent that can execute Python code.",
    handoff_description="Handle python related code executions.",
    model=model,
)

async def invoke_python_agent(ctx:RunContextWrapper, arg:str) -> Agent:
    """
    args: JSON string containing handoff input
    """

    data = json.loads(arg) # arg ko json mai convert karta hai
    print(f"[Handoff Triggered] Code received for execution: {data.get('code')}")
    # Yahan ap python code execute kar sakte hain, if you want
    return python_agent