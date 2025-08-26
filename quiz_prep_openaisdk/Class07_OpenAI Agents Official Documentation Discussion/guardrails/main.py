from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, RunConfig, ModelSettings, OutputGuardrailTripwireTriggered
from openai import AsyncOpenAI
import asyncio
from guardrails.input_guardrails import math_input_guardrail, physics_input_guardrail, coding_input_guardrail
from guardrails.output_guardrails import physics_output_guardrail,coding_output_guardrail, math_output_guardrail
from rich import print


load_dotenv()

enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

model1 = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

my_config = RunConfig(
    model=model,
    model_settings=ModelSettings(
        max_tokens=500,
        temperature=0.7,
    )
)
# Specialized Agents

## Math Agent
math_agent = Agent(
    name="MathAgent",
    instructions="""
    You are a specialized agent for performing mathematical calculations and solving math problems.
    """,
    model=model1,
    handoff_description="You task is to perform mathematical calculations and solve math problems delegated from main agent or any other specialized agents.",
    input_guardrails=[math_input_guardrail],
    output_guardrails=[math_output_guardrail],
)

## Physics Agent
physics_agent = Agent(
    name="PhysicsAgent",
    instructions="""
    You are a specialized agent for answering questions and solving problems related to physics.
    """,
    model=model1,
    handoff_description="You task is to answer questions and solve problems related to physics delegated from main agent or any other specialized agents.",
    input_guardrails=[physics_input_guardrail],
    output_guardrails=[physics_output_guardrail],
)

## Coding Agent
coding_agent = Agent(
    name="CodingAgent",
    instructions="""
    You are a specialized agent for writing and debugging code in python programming languages.
    """,
    model=model1,
    handoff_description="You task is to write and debug code in python programming languages delegated from main agent or any other specialized agents.",
    input_guardrails=[coding_input_guardrail],
    output_guardrails=[coding_output_guardrail],
)



# Main Agent
main_agent = Agent(
    name="MainAgent",
    instructions="""
    # Instructions
    - You are a helpful and creative assistant. You can perform tasks, delegate subtasks to other specialize agents.
    - You have access to the following specialized agents:
        - `MathAgent`: A specialized agent for performing mathematical calculations and solving math problems.
        - `PhysicsAgent`: A specialized agent for answering questions and solving problems related to physics.
        - `CodingAgent`: A specialized agent for writing and debugging code in python programming languages.
    - When you receive a task, you should first determine if it can be handled by one of the specialized agents. If so, delegate the task to the appropriate agent.
    - If the task is complex and requires multiple steps, break it down into smaller subtasks and delegate each subtask to the relevant specialized agent.
    - If the task cannot be handled by any specialized agent, you should handle it yourself.
    - Always provide clear and concise responses to the user.
    - If user asks something which is not related to the specialized agents, you should polietely apologize and refuse to handle the task.
    """,
    model=model,
    handoffs=[math_agent, physics_agent, coding_agent],
)

user_input = input("Enter your task: ")

async def main():
    try:
        result = await Runner.run(
            starting_agent=main_agent,
            input=user_input,
            run_config=my_config,
       )
        print("Final Output:", result.final_output)
        
    except OutputGuardrailTripwireTriggered:
        print("Output guardrail tripwire triggered. The output may violate guardrail policies.")
        


if __name__ == "__main__":
    asyncio.run(main())