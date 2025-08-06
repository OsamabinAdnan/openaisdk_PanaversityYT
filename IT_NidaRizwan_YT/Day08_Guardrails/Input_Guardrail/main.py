
from dotenv import load_dotenv
import os
import asyncio
from agents import (
    Agent, 
    Runner, 
    OpenAIChatCompletionsModel, 
    set_tracing_disabled, 
    RunConfig,
    input_guardrail,
    RunContextWrapper,
    TResponseInputItem,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
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

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="Check if the user is asking you to do their math homework",
    output_type=MathHomeworkOutput,
)

@input_guardrail
async def math_guardrail(
    ctx:RunContextWrapper[None], 
    agent:Agent, 
    input:str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        input_guardrail_agent,
        input,
        context=ctx.context,
        run_config=config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_math_homework,
    )


agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)

async def main():
    try:
        response =await Runner.run(
            agent,
            input="Hello, can you help me solve for x: 2x + 3 = 11?",
            run_config=config,
        )
        print("\nInput Guardrail didn't trip\n")
        print(response.final_output)
    
    except InputGuardrailTripwireTriggered:
        print("\nThis is Math homework! that's not allowed to be done. GUARDRAIL TRIPPED\n")

if __name__ == "__main__":
    asyncio.run(main())
    