import os
from dotenv import load_dotenv
from agents import Agent, ModelSettings, Runner, function_tool, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, handoff, GuardrailFunctionOutput, input_guardrail
from openai import AsyncOpenAI
from rich import print
import asyncio

load_dotenv()

# enable_verbose_stdout_logging()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

check_agent=Agent(
    name="Checker",
    instructions="You are a checker agent. You need to check if the user query is related to math.",
    model=llm_model,
)

@input_guardrail
async def input_guardrail_function(ctx, agent, input)-> GuardrailFunctionOutput:
    result = await Runner.run(
        check_agent,
        input
    )
    return GuardrailFunctionOutput(
         output_info=result.final_output,
         tripwire_triggered=result.final_output # It accepts boolean value but here we are passing string
)

async def main():

    main_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    input_guardrails=[input_guardrail_function],
    model=llm_model,
)
    
    try:
        result = await Runner.run(
            main_agent,
            "solve 2+ 5 - 6",
            )
        print(result.final_output)

    except Exception as ig:
        print(f"Exception raise: {type(ig).__name__} - {str(ig)}")


asyncio.run(main())