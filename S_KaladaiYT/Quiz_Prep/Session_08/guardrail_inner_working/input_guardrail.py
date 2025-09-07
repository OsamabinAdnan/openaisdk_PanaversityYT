import asyncio
import os
from typing import List
from dotenv import load_dotenv
from agents import (
    Agent, RunContextWrapper, Runner, OpenAIChatCompletionsModel, TResponseInputItem, set_tracing_disabled,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    enable_verbose_stdout_logging
    )
from openai import AsyncOpenAI
from pydantic import BaseModel
from rich import print


load_dotenv()
# set_tracing_disabled(disabled=True)
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)


# Class for output type
class MathOutput(BaseModel):
    is_math_related : bool
    reasoning : str


check_agent = Agent(
    name="Check Agent",
    instructions="Check if the user's input includes any math related question.",
    model=model,
    output_type=MathOutput,
)

@input_guardrail
async def input_guard_function(
    ctx:RunContextWrapper, 
    agent:Agent,
    input:str | List[TResponseInputItem]
) -> GuardrailFunctionOutput:
    """Input Guard Function"""
    result = await Runner.run(
        check_agent,
        input=input,
        context=ctx.context
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_math_related
    )

# Main Agent
customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    model=model,
    input_guardrails=[input_guard_function]
)


async def main():
    try:
        result = await Runner.run(
            customer_support_agent,
            # "Hello, can you help me solve for x: 2x + 3 = 11?"
            "Hello!"
        )
        print(result.final_output)
        print("\nGuardrail didn't trip - this is unexpected\n")
    except InputGuardrailTripwireTriggered as e:
        print("\nMath Homework Guardrail Tripwire Triggered\n")
        

if __name__ == "__main__":
    asyncio.run(main())