import os
from dotenv import load_dotenv
from agents import Agent, ModelSettings, Runner, function_tool, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, handoff
from openai import AsyncOpenAI
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

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

#is_enable False and check logs and than tool choice non

@function_tool
def weather_tool(city:str):
    """get the weather for given city"""

    return f"the current weather in {city} is cloudy"

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant.",
    tools=[weather_tool],
    model=llm_model,
    # model_settings=ModelSettings(
    #     tool_choice="none"
    # )
)

result = Runner.run_sync(
    main_agent,
    "what is current weather in karachi?",
    # max_turns=2
)

print(result.final_output)