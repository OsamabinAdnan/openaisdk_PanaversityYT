from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, RunConfig, ModelSettings, input_guardrail, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput
from openai import AsyncOpenAI
import asyncio
from pydantic import BaseModel
from typing import Any

load_dotenv()

# enable_verbose_stdout_logging()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model1 = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

my_config = RunConfig(
    model=model1,
    model_settings=ModelSettings(
        max_tokens=500,
        temperature=0.7,
    )
)

# Math Guardrail

class MathAgent(BaseModel):
    is_math_work : bool
    reasoning : str

math_guardrail_agent = Agent(
    name="MathGuardrailAgent",
    instructions="""
        Check if the user input asking help to solve a math problem of exam or quiz.
        - If yes, set is_math_work to True and provide reasoning.
        - If no, set is_math_work to False and provide reasoning.
    """,
    output_type=MathAgent,
    model=model1,
)

@input_guardrail
async def math_input_guardrail (
    ctx: RunContextWrapper[None], agent:Agent[Any], input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent= math_guardrail_agent,
        input=input,
        context=ctx.context,
        run_config=my_config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_work,
    )

# Physics Guardrail

class PhysicsAgent(BaseModel):
    is_physics_work : bool
    reasoning : str

physics_guardrail_agent = Agent(
    name="PhysicsGuardrailAgent",
    instructions="""
        Check if the user input asking help to solve a Physics problem of exam or quiz.
        - If yes, set is_physics_work to True and provide reasoning.
        - If no, set is_physics_work to False and provide reasoning.
    """,
    output_type=PhysicsAgent,
    model=model1,
)

@input_guardrail
async def physics_input_guardrail (
    ctx: RunContextWrapper[None], agent:Agent[Any], input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent= physics_guardrail_agent,
        input=input,
        context=ctx.context,
        run_config=my_config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_physics_work,
    )

# Coding Guardrail

class CodingAgent(BaseModel):
    is_coding_work : bool
    reasoning : str

coding_guardrail_agent = Agent(
    name="CodingGuardrailAgent",
    instructions="""
        Check if the user input asking help to solve a pyhton Coding problem of exam or quiz.
        - If yes, set is_coding_work to True and provide reasoning.
        - If no, set is_coding_work to False and provide reasoning.
    """,
    output_type=CodingAgent,
    model=model1,
)

@input_guardrail
async def coding_input_guardrail (
    ctx: RunContextWrapper[None], agent:Agent[Any], input: str | list[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent= coding_guardrail_agent,
        input=input,
        context=ctx.context,
        run_config=my_config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_coding_work,
    )