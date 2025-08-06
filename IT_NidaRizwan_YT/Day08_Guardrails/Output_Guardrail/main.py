
from dotenv import load_dotenv
import os
import asyncio
from agents import (
    Agent, 
    Runner, 
    OpenAIChatCompletionsModel, 
    set_tracing_disabled, 
    RunConfig,
    RunContextWrapper,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    output_guardrail,
)
from openai import AsyncOpenAI
from pydantic import BaseModel

load_dotenv()
set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# External Client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

class MessageOutput(BaseModel):
    response:str

class MathOutput(BaseModel):
    is_math:bool
    reasoning:str

output_guardrail_agent = Agent(
    name="output_guardrail_agent",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)

@output_guardrail
async def math_guardrail(
    ctx:RunContextWrapper,
    agent:Agent,
    output:MessageOutput,
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        output_guardrail_agent,
        output.response,
        context=ctx.context,
        run_config=config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math
    )

agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail],
    output_type=MessageOutput,
)

async def main():
    try:
        final_response = await Runner.run(
            agent,
            "Hello, what is Agentic AI?",
            run_config=config,
        )
        print("Guardrail didn't trip - this is unexpected")
        print(final_response.final_output)
    except OutputGuardrailTripwireTriggered:
        print("Math output guardrail tripped")

if __name__ == "__main__":
    asyncio.run(main())