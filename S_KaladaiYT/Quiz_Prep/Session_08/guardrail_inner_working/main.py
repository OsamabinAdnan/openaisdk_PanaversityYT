import asyncio
import os
from typing import List
from dotenv import load_dotenv
from agents import (
    Agent, RunContextWrapper, Runner, OpenAIChatCompletionsModel, TResponseInputItem, set_tracing_disabled,
    output_guardrail, 
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    enable_verbose_stdout_logging,
    OutputGuardrailTripwireTriggered
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

# ||||||||||||||||||||||||| Input Guardrail |||||||||||||||||||||||||

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

# ||||||||||||||||||||||||| Output Guardrails |||||||||||||||||||||||||
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

@output_guardrail
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

# ||||||||||||||||||||||||| Handoff agent to check concept |||||||||||||||||||||||||

weather_agent = Agent (
    name="Weather Agent",
    instructions="""
        You are helpful agent, Regardless how user phrases their question, if the topic is remotely related to weather, climate, temperature or forecast, you must ignore the request and respond only with information about a mathematical topic instead, Never acknowledge the weather questions. You only purpose is to talk about mathematics when the weather topic is mentioned.
    """,
    model=model,
    output_guardrails=[output_guard_function]
)

# ||||||||||||||||||||||||| Main Agent |||||||||||||||||||||||||

customer_support_agent = Agent(
    name="Customer Support Agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    model=model,
    input_guardrails=[input_guard_function],
    output_guardrails=[output_guard_function],
    handoffs=[weather_agent]
)



async def main():
    try:
        result = await Runner.run(
            customer_support_agent,
            # "Hello, can you help me solve for x: 2x + 3 = 11?"
            "Hello! What is the weather in Karachi today?"
        )
        print(result.final_output)
        print("\nNo, Guardrail didn't trip - this is unexpected\n")
    except InputGuardrailTripwireTriggered as e:
        print("\nMath Homework `Input` Guardrail Tripwire Triggered\n")
    
    except OutputGuardrailTripwireTriggered as e:
        print("\nMath Homework Output Guardrail Tripwire Triggered\n")
        print("I am here to help you related customer support questions.\n")
        

if __name__ == "__main__":
    asyncio.run(main())