from typing import Dict, TypedDict
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio, os
from agents import (
    Agent,
    AgentOutputSchema,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    enable_verbose_stdout_logging,
    input_guardrail,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    set_tracing_export_api_key
)
from agents.run import RunConfig
from rich import print
from dataclasses import dataclass

load_dotenv()

# enable_verbose_stdout_logging()

tracking_api_key = os.environ["OPENAI_API_KEY"]
set_tracing_export_api_key(tracking_api_key)

MODEL_NAME = "gemini-2.5-flash" # which LLM model will agent use

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY is not set")

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise Exception("BASE_URL is not set")


# external_client is the connection that allows us to talk with Gemini API
external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY,
        base_url = BASE_URL, #it is Gemini api endpoint bcx we are using Gemini LLM in OpenAI Agents framework
)

model = OpenAIChatCompletionsModel(
        model = MODEL_NAME,
        openai_client=external_client, #connect external cient with OpenAI client
)

config = RunConfig(
    model=model,
)

# pydatic class
class DevOutput(BaseModel):
    html: str
    css: str


agent = Agent(  
    name="developer agent",
    instructions="You are a developer agent. You help users with development questions.",
    model=model,
    output_type=AgentOutputSchema( # use AgentOutputSchema if you want to disable strict JSON schema
        output_type=DevOutput,
        strict_json_schema=True,
    )
)

async def main():
    
    result = await Runner.run(agent, "what is HTML and CSS?", run_config=config)
    print(result.final_output)

asyncio.run(main())