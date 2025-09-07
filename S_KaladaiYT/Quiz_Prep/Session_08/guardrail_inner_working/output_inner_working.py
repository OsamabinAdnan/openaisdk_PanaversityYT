import asyncio
import os
from typing import List
from dotenv import load_dotenv
from agents import (
    Agent, OutputGuardrail, RunContextWrapper, Runner, OpenAIChatCompletionsModel, TResponseInputItem, set_tracing_disabled,
    output_guardrail,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    enable_verbose_stdout_logging,
    OutputGuardrailResult
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

class OutputMath(BaseModel):
    is_math_related : bool
    reasoning : str

class MessageOutput(BaseModel): 
    result: str

output_guard_agent = Agent(
    name="Output Guard Agent",
    instructions="You are an output guard agent. You check if the output is math related.",
    model=model,
    output_type=OutputMath
)

async def output_guard_function(ctx:RunContextWrapper, agent:Agent, output:MessageOutput) -> GuardrailFunctionOutput:
    """Output Guard Function"""
    result = await Runner.run(
        output_guard_agent,
        output,
        context=ctx.context
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_math_related
    )

# |||||||||||||||||||||||| Making output guardrail from class OuputGuardrail class ||||||||||||||||||||||||
check_output_agent = OutputGuardrail(
    name="Check_output",
    guardrail_function=output_guard_function
)

# Main Agent
customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    model=model,
    output_guardrails=[check_output_agent]
)


async def main():
    """Runner"""
    try:
        result = await Runner.run(
            customer_support_agent,
            "Hello, can you help me solve for x: 2x + 3 = 11?"
            # "Hello!",
        )
        print(result.final_output)
        print("\nGuardrail didn't trip - this is unexpected\n")

    except OutputGuardrailTripwireTriggered as e:
        print("\nMath Homework Output Guardrail Tripwire Triggered\n")
        print("I am here to help you related customer support questions.\n")

        
if __name__ == "__main__":
    asyncio.run(main())