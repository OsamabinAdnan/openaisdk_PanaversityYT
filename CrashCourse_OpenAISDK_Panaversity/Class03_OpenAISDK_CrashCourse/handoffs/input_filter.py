import asyncio
import os
from typing import Any
from dotenv import load_dotenv
from agents import Agent, RunContextWrapper, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, handoff
from openai import AsyncOpenAI
from agents.extensions import handoff_filters
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

# Class for is_enabled context
class CurrentUser(BaseModel):
    is_logged_in: bool

refund_agent = Agent(
    name="Refund agent",
    instructions="You are a refund agent. Answer related to refund questions.",
    model=llm_model,
    handoff_description="You are a refund agent. You work on user refund queries related to order.",
)

async def refund_agent_enabler(local_context:RunContextWrapper[CurrentUser], agent:Agent) -> bool:
    print(f"local_context: {local_context.context}")
    print(f"agent: {agent.name}")
    if local_context.context and local_context.context.is_logged_in:
        return True
    return False


handoff_object = handoff(
    agent=refund_agent,
    tool_name_override="order_refund_tool",
    tool_description_override="You are order refund tool, you work on refund queries related to order.",
    is_enabled=refund_agent_enabler,
    input_filter=handoff_filters.remove_all_tools
)

triage_agent = Agent(
    name="Triage agent", 
    handoffs=[handoff_object],
    instructions="You are a triage agent. You work is to delegate querys to the appropriate agent. Appropriate agents show exist otherwise you will answer him",
    model=llm_model
)

async def main():
    current_user = CurrentUser(is_logged_in=True)
    result = await Runner.run(
        triage_agent, 
        "I want to refund my order, order details are following: Order ID: 12345, Order amount: $100.00, Order date: 2022-01-01, reason: I don't like the product, and I have product in my hands",
        # "hi, how are you?"
        context=current_user
    )

    print(f"\nResponse:{result.final_output}")
    print(f"\nLast agent: {result.last_agent.name}\n")

if __name__ == "__main__":
    asyncio.run(main())