import os
from dotenv import load_dotenv
from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunContextWrapper, Runner, OpenAIChatCompletionsModel, TResponseInputItem, function_tool, enable_verbose_stdout_logging, ModelSettings, UserError, input_guardrail
from openai import AsyncOpenAI
from rich import print
from pydantic import BaseModel
import asyncio

load_dotenv()

# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")


my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model_25 = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

model_20 = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=my_client,
)

# Class for input guardrail exception
class MathHomeWork(BaseModel):
    is_math_homework: bool
    reasoning:str

input_guardrail_agent = Agent(
    name="Input Guardrail Agent",
    instructions="""
        Check if the user is asking you to do math homework or solve any math problem.
    """,
    model=model_20,
    output_type=MathHomeWork,
)

@input_guardrail
async def input_math_guardrail(ctx:RunContextWrapper[None], agent:Agent, input:str | list [TResponseInputItem])-> GuardrailFunctionOutput:
    result = await Runner.run(
        input_guardrail_agent,
        input,
        context=ctx.context,
    )
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )

async def main():
    main_agent = Agent(
        name="Main Agent",
        instructions="""
            You are helpful assistant
            - if user asks about weather, call get_weather function
        """,
        model=model_25,
        input_guardrails=[input_math_guardrail],
    )

    try:
        result = await Runner.run(
            main_agent,
            """Solve x:
                - 2x + 3 = 5x - 11 
            """, # Input that will raise input guardrail exception
        )

        print(result.final_output)

    # Uncomment below lines to see exception using general Exception class
    # except Exception as IGT:
    #     print(f"\nException raised, exception type: {type(IGT).__name__} - {str(IGT)}\n")
    
    except InputGuardrailTripwireTriggered as IGT:
        print(f"\nException raised: {IGT}\n")

if __name__ == "__main__":
    asyncio.run(main())