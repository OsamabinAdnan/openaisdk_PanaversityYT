import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()
set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model,
)

result = Runner.run_sync(
    agent,
    input="Hello, how are you?",
    run_config=config,
)

print("\nCalling Agent\n")
print(result.final_output)