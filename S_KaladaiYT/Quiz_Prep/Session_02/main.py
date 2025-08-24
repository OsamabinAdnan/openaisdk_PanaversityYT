from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled, AgentBase, RunContextWrapper, enable_verbose_stdout_logging, Handoff
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from rich import print
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, List

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

run_config = RunConfig(
    model=model,
)

# Dynamic instructions function
python_agent = Agent(
    name="PythonAgent",
    instructions="You are a Python agent that can execute Python code.",
    handoff_description="Handle python related code executions.",
    model=model,
)

main_agent = Agent(
    name="MainAgent",
    instructions="""
        - You are the main agent that can delegate tasks to specialized agents.
        - If query is related to Python code execution, delegate it to the PythonAgent.
        - Otherwise, dont answer query which are not related to python and politely apologize and say "I'm sorry, I don't know how to help with that.".
    """,
    model=model,
    # handoffs=[python_agent],
    handoff = Handoff (
        agent_name="PythonAgent",

    )
)

result = Runner.run_sync(
    main_agent,
    "What is OOPs in Python? explain in maximum 4 lines?",
    run_config=run_config,
)

print(result.final_output)
print(result.last_agent.name)
# https://youtu.be/PbreiBOPxFk?t=2110