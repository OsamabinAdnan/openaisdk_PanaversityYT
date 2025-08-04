import os
import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("Missing GEMINI_API_KEY environment variable")

MODEL = "gemini-2.0-flash"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
    model=model,
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
    model=model
)


orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions="You are a translation agent. You use the tools given to you to translate."
    "If asked for multiple translations, you call the relevant tools.",
    model=model,
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        )
    ],
    )

async def main():
    result = await Runner.run(
        orchestrator_agent,
        input="Say 'Hello, how are you?' in French.",
        run_config=config,
    )

    print("\nCalling Agent\n")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())