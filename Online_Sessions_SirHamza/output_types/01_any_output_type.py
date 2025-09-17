from typing import Dict
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

load_dotenv()

enable_verbose_stdout_logging()

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

agent = Agent(
    name="developer agent",
    instructions="You are a developer agent. You help users with development questions.",
    model=model,
    output_type=list[str]
)

async def main():
    
    result = await Runner.run(
        agent, 
        "what is HTML and CSS?", 
        run_config=config
    )
    
    print(result.final_output)

asyncio.run(main())

# agent always return plain-text (str) by-default
# by default the value of output_type is None
# we can customize it by using output_type

# output-type could be "Any" type or a "pydantic class or dataclass" or a custom type like AgentOutputSchemaBase or AgentOutputSchema 


# some basic output_types:

# output_type=bool 
# output_type=int
# output_type=list[str]


# for dict you need to disable strict schema for that you have to use AgentOutputSchema and a class
# class DevOutput(BaseModel):
#     html: str
#     css: str
    
# AgentOutputSchema(DevOutput, strict_json_schema=False)  