from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging
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

# Weather Agent
weather_agent = Agent(
    name="WeatherAgent",
    instructions="You are a weather agent. You can provide weather information for any location user asks for. Use the web search tool to find current weather information.",
    model=model
)


# Create main agent with basic instructions
agent: Agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant!",
    model=model,
    handoffs=[weather_agent], # handoff parameter of Agent class takes a list of agents to which it can handoff the conversation
)

# Run the agent synchronously with a test question
result = Runner.run_sync(
    agent,
    "What is current weather in Karachi?",
)

print("\nCALLING AGENT")
print("=" * 50)

print(result.final_output)