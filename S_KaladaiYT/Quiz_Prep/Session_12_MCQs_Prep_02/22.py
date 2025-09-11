import os
from dotenv import load_dotenv
from agents import Agent, HandoffInputData, RunConfig, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, function_tool, handoff
from openai import AsyncOpenAI
from rich import print

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

my_config = RunConfig(
    model=model,
    group_id="my_test",
)

@function_tool()
def get_weather(city:str):
    return f"The weather in {city} is sunny"

@function_tool
def add_numbers(a:int, b:int):
    return a + b

python_agent = Agent(
    name="Python Agent",
    instructions="""
        You are helpful assistant and expert in Python.
        - if user ask any question related to python, then you will answer
    """,
    model=model,
)

def handoff_filter() -> HandoffInputData:
    """
    This is an example input filter.
    It can modify the data that the next agent receives.
    For example, you could remove previous turns of the conversation.
    """
    print("--- Running input filter ---")
    # For now, let's just return the data unmodified
    return

python_agent_handoff = handoff (
    agent=python_agent,
    input_filter=handoff_filter(),
)

main_agent = Agent(
    name="Main Agent",
    instructions="""
        You are helpful assistant.
        - if user ask for weather, then delegate to weather tool
        - if user ask for addition, then delegate to add_numbers tool
        - if user ask any question related to python, then delegate to python_agent_handoff
    """,
    model=model,
    tools=[get_weather, add_numbers],
    handoffs=[python_agent_handoff],
)

result = Runner.run_sync(
    main_agent,
    "What is OOPs in Python? 2 to 4 lines",
    run_config=my_config,
)

print(f"\n{result.final_output}\n")

