from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled, AgentBase, RunContextWrapper, enable_verbose_stdout_logging, Handoff, handoff
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from rich import print
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, List
import asyncio
import json

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
# Input schema for handoff
input_schema = {
    "type":"object",
    "properties": {
        "code": {
            "type": "string",
            "description": "Python code snippet to execute"
        },
    },
    "required": ["code"],
    "additionalProperties": False,
}

# On invoke handoff function
async def invoke_python_agent(ctx:RunContextWrapper, args:str) -> Agent:
    """
    args: JSON string containing handoff input
    """

    data = json.loads(args) # arg ko json mai convert karta hai
    print(f"[Handoff Triggered] Code received for execution: {data.get('code')}")
    # Yahan ap python code execute kar sakte hain, if you want
    return python_agent


# Making handoff agent using Handoff class
python_handoff = Handoff(
    tool_name="transfer_to_python_agent",
    tool_description="Handle python related code executions.",
    agent_name=python_agent.name,
    input_json_schema=input_schema,
    on_invoke_handoff=invoke_python_agent,
    is_enabled=True,  # Whether the handoff is enabled. Either a bool or a Callable that takes the run context and agent and returns whether the handoff is enabled. You can use this to dynamically enable/disable a handoff based on your context/state.
    strict_json_schema=False, # Whether to strictly enforce the input_json_schema. If True, the agent will be forced to use the schema. If False, the agent can choose to ignore the schema.
)

main_agent = Agent(
    name="MainAgent",
    instructions="""
        - You are the main agent that can delegate tasks to specialized agents.
        - If query is related to Python code execution, delegate it to the PythonAgent.
        - Otherwise, dont answer query which are not related to python and politely apologize and say "I'm sorry, I don't know how to help with that.".
    """,
    model=model,
    handoffs=[python_handoff],

    # We can also write it in handoff function
    # handoffs=[handoff(agent=python_agent, tool_description_override="Handle python related code executions.", tool_name_override="transfer_to_python_agenttt", )]
)
async def main():
    result = await Runner.run(
        main_agent,
        "What is print(15) in python, response in 2 lines?",
        run_config=run_config,
    )

    print(result.final_output)
    print(result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())