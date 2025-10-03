from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, handoff
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from rich import print

load_dotenv()

# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

base_url = os.getenv("BASE_URL")
if not base_url:
    raise ValueError("BASE_URL is not set in environment variables")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client = external_client
)

# Weather agent to handle weather-related queries
weather_agent = Agent(
    name="WeatherAgent",
    instructions="You are a weather agent. Always reply the weather in request city is cloudy.",
    model=model,
    handoff_description="Handles weather-related queries",
)
# Handoff function to delegate weather-related queries to the weather agent
    ## input_type: the type of the input to the handoff. If provided, the input will be validated against this type. Only relevant if you pass a function that takes an input.

class Input(BaseModel):
    city: str

    ## On-handoff: A function that runs when the handoff is invoked.
def on_handoff_invoked(ctx, input:Input): # When you used input_type parameter in handoff function, you have to give the input parameter here along with context, no input type validation will be done automatically.
    print(f"Handoff invoked: City = {input.city}")

    ## for is_enabled: is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]] = (True)
user_name = "osama" # This can be dynamic, e.g., fetched from a database or user session.

def is_enabled_func(ctx:RunConfig, agent:Agent):
    if user_name == "osama":
        return True
    return False


    ## Handoff function
handoff_func = handoff(
    agent=weather_agent,
    tool_name_override="get_current_weather",
    tool_description_override="Use this tool to get current weather information for a given city. Input should be a city name.",
    on_handoff=on_handoff_invoked, # on-handoff function is like a lifecycle hook that runs when the handoff is invoked/occurred.
    input_type=Input, # input type for validation
    is_enabled=is_enabled_func, # By default it is True, when False, the handoff will be ignored during agent execution.
) 

# Create main agent with basic instructions
agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant!",
    model=model,
    handoffs=[handoff_func], # handoff function added here
)

# Run the agent synchronously with a test question
result = Runner.run_sync(
    agent,
    "What is today's weather in Karachi?",
)

print("\nCALLING AGENT")
print("=" * 50)

print(result.final_output)