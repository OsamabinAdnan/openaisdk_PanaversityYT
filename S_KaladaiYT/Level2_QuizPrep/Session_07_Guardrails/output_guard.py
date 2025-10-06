import asyncio
import os
from typing import Any
from dotenv import load_dotenv
from agents import Agent, RunContextWrapper, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, output_guardrail, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered
from openai import AsyncOpenAI
from rich import print
from pydantic import BaseModel

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

# 3. Class for input guardrail
class MathOutput(BaseModel):
    is_math_output: bool
    reasoning: str

# 4. Input Guardrail Agent
output_guardrail_agent = Agent(
    name="Output Guardrail Agent",
    instructions="Determine if the output is a math problem. If it is, set is_math_input to true and provide reasoning. If not, set is_math_input to false and provide reasoning.",
    model=llm_model,
    output_type=MathOutput,
)

# 5. Input Guardrail Function
@output_guardrail
async def math_output_guardrail(
    ctx:RunContextWrapper, agent: Agent[Any], output: str
) -> GuardrailFunctionOutput:
    response = await Runner.run(
        output_guardrail_agent,
        output,
        context=ctx.context,
    )

    return GuardrailFunctionOutput(
        output_info=response.final_output.reasoning,
        tripwire_triggered=response.final_output.is_math_output,
    )

async def main():
    main_agent = Agent(
        name="Assistant",
        instructions="You are helpful assistant.",
        model=llm_model,
        output_guardrails=[math_output_guardrail],
    )

    try:
        result = await Runner.run(
            main_agent,
            "What is derivative of x^2?",
        )

        print(result.final_output)
    except OutputGuardrailTripwireTriggered as e:
        print(f"Output Guardrail Triggered: {e.guardrail_result}")

if __name__ == "__main__":
    asyncio.run(main())