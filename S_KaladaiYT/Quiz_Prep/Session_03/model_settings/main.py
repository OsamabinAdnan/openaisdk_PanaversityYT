from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, RunConfig,  enable_verbose_stdout_logging, ModelSettings
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
# from rich import print
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Any, List
import asyncio
import json
import pprint
import tiktoken

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
    model="gemini-2.5-flash-lite",
    openai_client=external_client,
)

run_config = RunConfig(
    model=model,
)

agent = Agent(
    name="Assitant",
    instructions="You are a helpful assistant.",
    model=model,
    model_settings=ModelSettings(
        temperature=0.5,
        max_tokens=200,
        top_p=0.3, # Value should be less than equal to 1.0 |  # Use only top 30% of vocabulary
        # frequency_penalty=0.25, # Avoid repeating words
        presence_penalty=0.25, # Encourage new topics
    )
)

result = Runner.run_sync(
    agent,
    "Sun is...",
    run_config=run_config,
)

print(f"\n{result.final_output}\n")

# enc = tiktoken.get_encoding("cl100k_base")  # encoding used by GPT-4, GPT-3.5
# tokens = enc.encode("Hello, world!")
# print(tokens)          # token IDs
# print(len(tokens))     # number of tokens
# print(enc.decode(tokens))
