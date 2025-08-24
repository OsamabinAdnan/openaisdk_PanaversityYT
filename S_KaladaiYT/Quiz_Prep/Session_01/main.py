from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled, AgentBase, RunContextWrapper
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
from rich import print
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, List

load_dotenv()

# set_tracing_disabled(True)


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
    # tracing_disabled=True,
)

# Dynamic instructions function
def dynamic_instructions(context: RunContextWrapper, agent: Agent) -> str:
    return f"You are {agent.name}. Adapt to the user's needs."

agent = Agent(
    name="Assistant",
    # instructions=dynamic_instructions,
    model=model,
    # Prompt 
    prompt={
        "id": "pmpt_68a9aebde7a08194a7f6d3f08c0310980db39709860bbc40",
        "version": "3",
        "variables": {
            "topic": "python"
        }
    }
)

result = Runner.run_sync(
    agent,
    input= "Hello",
    run_config=run_config,
)

print(result.final_output)
print(result.last_agent.name)
