import os
from dotenv import load_dotenv
from rich import print
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, ModelSettings, enable_verbose_stdout_logging
from openai.types.shared import Reasoning
from openai import AsyncOpenAI

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

@function_tool
def get_weather(location: str) -> str:
    """Get the current weather for a given location."""
    # Dummy implementation for illustration
    return f"The current weather in {location} is sunny with a temperature of 25°C."

@function_tool
def OBA () -> str:
    """Get info about Osama Bin Adnan."""
    return "Osama Bin Adnan is a fictional character often used in examples. He is not a real person."

setting = ModelSettings(
    temperature=0.7,
    top_p=0.9,
)

setting_override = setting.resolve(
    override=ModelSettings(
        temperature=0.3,
        top_p=0.5,
    )
)

# Main Agent
base_agent: Agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=llm_model,
    model_settings=setting_override,
    tools=[get_weather, OBA],
)

result = Runner.run_sync(
    base_agent,
    "What is Agent in LLM? in 3 lines",
    # "What is the weather in New York? Also, who is Osama Bin Adnan?"
)
print(f"Agent Response: {base_agent.name}")
print("=" * 30)
print(f"\n{result.final_output}\n")
print(setting_override.to_json_dict())