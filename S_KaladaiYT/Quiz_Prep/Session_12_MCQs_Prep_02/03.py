import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, function_tool,ModelSettings, Handoff, trace, set_trace_processors, FunctionSpanData
from openai import AsyncOpenAI
from rich import print
import pprint
from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor, default_processor



load_dotenv()
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

exporter = ConsoleSpanExporter()
processor = BatchTraceProcessor(exporter=exporter)
set_trace_processors([processor, default_processor()])


@function_tool()
def get_weather(city:str):
    return f"The weather in {city} is sunny"

@function_tool
def add_numbers(a:int, b:int):
    return a + b

main_agent = Agent(
    name="Main Agent",
    instructions="""
        You are helpful assistant.
        - if user ask for weather, then delegate to weather tool
        - if user ask for addition, then delegate to add_numbers tool
    """,
    model=model,
    tools=[get_weather, add_numbers],
)
with trace(workflow_name="Osama workflow", trace_id="trace_01"):
    result = Runner.run_sync(
        main_agent,
        "What is current weather in Karachi?"
    )

pprint.pprint(f"\n{result.final_output}\n")

