import os
from dotenv import load_dotenv
from agents import Agent, MaxTurnsExceeded, Runner, OpenAIChatCompletionsModel, function_tool, AgentsException, UserError, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from rich import print

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

@function_tool
def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny"

main_agent = Agent(
    name="Main Agent",
    instructions="""
        You are helpful assistant
        - if user asks about weather, call get_weather function
    """,
    tools=[get_weather],
    model=model_25,
)

try:
    result = Runner.run_sync(
        main_agent,
        "What is current weather in Karachi?",
        max_turns=1,
    )

    print(result.final_output)

# Below exception will not raised because it is `UserError` exception but in out code it is raised as `AgentsException` or `MaxTurnsExceeded`
except UserError as error:
    print(f"Exception raised: {error}")

except AgentsException as error:
    print(f"Exception raised: {error}")

except MaxTurnsExceeded as error:
    print(f"Max turns error raised: {error}")
