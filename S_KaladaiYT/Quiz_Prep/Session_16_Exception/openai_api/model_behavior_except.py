import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging, ModelSettings, ModelBehaviorError
from rich import print

load_dotenv()

# enable_verbose_stdout_logging()


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
    model="gpt-3.5-turbo",
    model_settings=ModelSettings(
        tool_choice="weather_get" # Giving wrong tool name will raise ModelBehaviorError
    )
)

try:
    result = Runner.run_sync(
        main_agent,
        "What is current weather in Karachi?",
    )

    print(result.final_output)

# We can used below as well

# except Exception as MBE:
#     print(f"Exception raised: {type(MBE).__name__} - {str(MBE)}")

# But for simple ModelBehaviorError exception we can use ModlelBehaviorError class, so if any error occurs in model behavior, it will raise ModelBehaviorError

except ModelBehaviorError as MBE:
    print(f"Exception raised: {MBE}")
