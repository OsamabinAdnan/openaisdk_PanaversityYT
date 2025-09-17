import os
from dotenv import load_dotenv
from agents import Agent, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered, RunContextWrapper, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, output_guardrail
from openai import AsyncOpenAI
from rich import print
from pydantic import BaseModel
import asyncio

load_dotenv()

# enable_verbose_stdout_logging()


class MessageOutput(BaseModel):
    response: str

# Class for input guardrail exception
class MathHomeWork(BaseModel):
    is_math_homework: bool
    reasoning:str

output_guardrail_agent = Agent(
    name="Output Guardrail Agent",
    instructions="""
        Check if the final output is about math homework or solve any math problem.
    """,
    model="gpt-4o",
    output_type=MathHomeWork,
)

@output_guardrail
async def output_math_guardrail(ctx:RunContextWrapper, agent:Agent, output:MessageOutput)-> GuardrailFunctionOutput:
    result = await Runner.run(
        output_guardrail_agent,
        output,
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
        model="gpt-4o",
        output_guardrails=[output_math_guardrail],
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
    
    except OutputGuardrailTripwireTriggered as OGT:
        print(f"\nException raised: {OGT}\n")
    
if __name__ == "__main__":
    asyncio.run(main())