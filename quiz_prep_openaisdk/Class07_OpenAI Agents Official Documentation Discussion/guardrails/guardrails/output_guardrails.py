from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, RunConfig, ModelSettings, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput, output_guardrail
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

class MessageOutput(BaseModel):
    response: str

#  Math Output Guardrail
class MathOutputAgent(BaseModel):
    response: str
    is_math_work: bool

math_guardrail_agent = Agent(
    name="MathOutputGuardrailAgent",
    instructions="""
        Check the output from Agent.
        - if output in appropriate to Maths, then its fine.
        - If output is not appropriate to Maths, then set is_math_work to True and provide reasoning.
        - Check any inappropriate content.
    """,
    output_type=MathOutputAgent,
    model=model1,
)

@output_guardrail
async def math_output_guardrail (
    ctx: RunContextWrapper[None], agent:Agent[Any], output: MessageOutput
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(
        math_guardrail_agent,
        output,
        context=ctx.context,
        run_config=my_config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_work,
    )

#  Physics Output Guardrail

class PhysicsOutputAgent(BaseModel):
    response: str
    is_physics_work: bool

physics_guardrail_agent = Agent(
    name="PhysicsOutputGuardrailAgent",
    instructions="""
        Check the output from Agent.
        - if output in appropriate to Physics, then its fine.
        - If output is not appropriate to Physics, then set is_physics_work to True and provide reasoning.
        - Check any inappropriate content.
    """,
    output_type=PhysicsOutputAgent,
    model=model1,
)

@output_guardrail
async def physics_output_guardrail (
    ctx: RunContextWrapper[None], agent:Agent[Any], output: MessageOutput
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(
        physics_guardrail_agent,
        output,
        context=ctx.context,
        run_config=my_config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_physics_work,
    )

#  Coding Output Guardrail

class CodingOutputAgent(BaseModel):
    response: str
    is_coding_work: bool

coding_guardrail_agent = Agent(
    name="CodingOutputGuardrailAgent",
    instructions="""
        Check the output from Agent.
        - if output in appropriate to Python Coding, then its fine.
        - If output is not appropriate to Python Coding, then set is_coding_work to True and provide reasoning.
        - Check any inappropriate content.
    """,
    output_type=CodingOutputAgent,
    model=model1,
)

@output_guardrail
async def coding_output_guardrail (
    ctx: RunContextWrapper[None], agent:Agent[Any], output: MessageOutput
    ) -> GuardrailFunctionOutput:
    result = await Runner.run(
        coding_guardrail_agent,
        output,
        context=ctx.context,
        run_config=my_config,
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_coding_work,
    )