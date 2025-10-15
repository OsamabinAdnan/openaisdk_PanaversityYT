import os
from dotenv import load_dotenv
from rich import print
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, handoff, set_tracing_disabled, ModelSettings, function_tool, enable_verbose_stdout_logging
from openai import AsyncOpenAI
import asyncio

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

proof_reader_agent = Agent(
    name="Proof Reader Agent",
    instructions="You are proof reader agent, provide your insight about the output of main agent, proof read it and remove unauthentic info from it and provide real factual result.",
    model=llm_model,
)


main_agent = Agent(
    name="Main Agent",
    instructions="You are main agent, answer the user query.",
    model=llm_model,
)

result_main_agent = Runner.run_sync (
    main_agent,
    "What is LLMs (Large Language Models), explain in short paragraph?",
)

print(f"[bold green]Main Agent Result:[/bold green] {result_main_agent.final_output}")

result_proof_reader_agent = Runner.run_sync (
    starting_agent= proof_reader_agent,
    input=result_main_agent.final_output,
)

print(f"[bold green]Proof Reader Agent Result:[/bold green] {result_proof_reader_agent.final_output}")