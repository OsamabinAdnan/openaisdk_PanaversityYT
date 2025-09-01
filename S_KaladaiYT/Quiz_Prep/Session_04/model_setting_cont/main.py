from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig,  enable_verbose_stdout_logging, ModelSettings
from openai import AsyncOpenAI
from openai.types.shared import Reasoning
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

agent = Agent(
    name="Assitant",
    instructions="You are a helpful assistant. Give complete answer of query in allocated max tokens.",
    model=model,
    model_settings=ModelSettings(
    #    max_tokens =100, # You have to give atleast 16 tokens in using OpenAI API, otherwise it will throw Bad request error

    #    reasoning=Reasoning(
    #        summary=["concise"],
    #    ),
    
    #   metadata={
    #   "live": "session#04"
    #   },

    #   store=False
    temperature=0.5
    )
)

result = Runner.run_sync(
    agent,
    "Hello! How can I help you today?",
    run_config=run_config,
)

print(f"\n{result.final_output}\n")
print(agent.model_settings.to_json_dict())
print(agent.model_settings.resolve(override=ModelSettings(
    temperature=1.0
)))


