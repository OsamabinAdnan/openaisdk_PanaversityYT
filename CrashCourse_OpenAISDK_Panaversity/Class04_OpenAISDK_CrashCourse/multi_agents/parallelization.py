import asyncio
import uuid
import os
from dotenv import load_dotenv
from rich import print
from agents import Agent, Runner, OpenAIChatCompletionsModel, RawResponsesStreamEvent, TResponseInputItem, trace, enable_verbose_stdout_logging, ItemHelpers
from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent
from openai import AsyncOpenAI



load_dotenv()

# enable_verbose_stdout_logging()
"""
This example shows the parallelization pattern. We run the agent three times in parallel, and pick
the best result.
"""

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

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    model=llm_model,
)

translation_picker = Agent(
    name="translation_picker",
    instructions="You pick the best Spanish translation from the given options.",
    model=llm_model,
)

async def main():
    msg = input("Hi! Enter a message, and we'll translate it to Spanish.\n\n")

    # Ensure the entire workflow is a single trace
    with trace("Parallel translation"):
        res_1, res_2, res_3 = await asyncio.gather(
            Runner.run(spanish_agent, msg),
            Runner.run(spanish_agent, msg),
            Runner.run(spanish_agent, msg),
        )

        output = [
            ItemHelpers.text_message_outputs(res_1.new_items),
            ItemHelpers.text_message_outputs(res_2.new_items),
            ItemHelpers.text_message_outputs(res_3.new_items),
        ]

        translations ="\n\n".join(output)
        print(f"\n\nTranslations:\n\n{translations}")

        best_translation = await Runner.run(
            translation_picker,
            f"Input: {msg}\n\nTranslations:\n{translations}",
        )

        print("\n\n ----")

        print(f"Best translation: {best_translation.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
