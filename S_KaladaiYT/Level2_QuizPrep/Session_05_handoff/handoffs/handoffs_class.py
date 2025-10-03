from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, Handoff
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

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
    instructions="You are a weather agent. You can provide current weather information for any city. Use the web search tool to find current weather information.",
    model=model,
)

# Schema for handoff input json schema
MY_SCHEMA = {
    "additionalProperties": False,
    "type": "object",
    "properties": {
        "city": {
            "type": "string",
        }
    },
    "required": ["city"],
}

# Invoke handoff function to transfer the conversation to the weather agent
async def invoke_handoff(ctx, input):
    return weather_agent

# Create a handoff object to transfer to a weather agent
handoff_object = Handoff(
    tool_name="transfer_to_weather_agent",
    tool_description="Use this tool to transfer the conversation to a weather agent.",
    input_json_schema= MY_SCHEMA,
    on_invoke_handoff= invoke_handoff,
    agent_name="Weather_Agent",
)


# Create main agent with basic instructions
agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant!",
    model=model,
    handoffs=[handoff_object],
)

# Run the agent synchronously with a test question
result = Runner.run_sync(
    agent,
    "What is current weather in Karachi?",
)

print("\nCALLING AGENT")
print("=" * 50)

print(result.final_output)