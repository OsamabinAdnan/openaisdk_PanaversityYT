from agents import Agent, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
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


# Configure the runner with model settings
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=False  # Disable tracing for simpler output
)

# Dynamic Instructions function for instructions

subject = input("Enter the subject for the assistant: ")
async def prompt(ctx, agent) -> str:
    if subject == "pyhton":
        return "You are a python coding assistant, always response about python"
    elif subject == "java":
        return "You are a java coding assistant always response about java"
    elif subject == "javascript":
        return "You are a javascript coding assistant always response about javascript"
    elif subject == "typescript":
        return "You are a typescript coding assistant always response about typescript"
    elif subject == "Nextjs" or subject == "nextjs" or subject == "next.js" or subject == "Next.js":
        return "You are a Next.js coding assistant always response about Next.js"
    else:
        return "You are a helpful assistant always response about user input"

# Create an AI agent with basic instructions
agent: Agent = Agent(
    name="Assistant",
    instructions=prompt,
    model=model
)

# Run the agent synchronously with a test question
result = Runner.run_sync(
    agent,
    "Hello, how are you?",
    run_config=config,
)

print("\nCALLING AGENT")
print("=" * 50)

print(result.final_output)