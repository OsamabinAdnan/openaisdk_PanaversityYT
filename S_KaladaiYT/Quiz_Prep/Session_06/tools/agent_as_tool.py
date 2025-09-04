from agents import Agent, FunctionToolResult, ModelSettings, RunContextWrapper, Runner, ToolsToFinalOutputResult, function_tool, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from rich import print
from typing import Any
from datetime import datetime
from agents.agent import StopAtTools

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

python_agent = Agent(
    name="Python_Agent",
    instructions="You are expert in Python Programming Language.",
    model=model,
)

agent = Agent(
    name="Assitant",
    instructions="""
    You are a helpful assistant. Give complete answer of user query.
    - if user's query is related to python programming language, use python_agent tool.
    """,
    model=model,
    model_settings=ModelSettings(
        max_tokens=200,
        tool_choice="required",
    ),
    tools=[
        python_agent.as_tool(
            tool_name="python_agent",
            tool_description="Your expert in Python Programming Language.",
        )
    ]
)

result = Runner.run_sync(
    agent,
    "What is OOPs in python, explain briefly in 3 to 4 lines.",
    # "Hello",
    run_config=run_config,
)

print(f"\n{result.final_output}\n")
