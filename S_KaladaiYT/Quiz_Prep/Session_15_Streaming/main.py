from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, ModelSettings, enable_verbose_stdout_logging
from openai.types.responses import ResponseTextDeltaEvent
from openai import AsyncOpenAI
from rich import print
from dataclasses import dataclass
import asyncio


load_dotenv()
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model_25 = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

model_20 = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=my_client,
)

async def main():

    main_agent = Agent(
        name="Joker",
        instructions="""
            You are a helpful assistant.
        """,
        model=model_25,
    )

    result = Runner.run_streamed(
        main_agent,
        "What is Agentic AI? explain within 200 words",
    )

    async for event in result.stream_events():
        # print(event) # It will show all events of stream events
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end=" ", flush=True) 
            # Normally, Python’s print() writes output to a buffer first (not directly to the terminal).
            # The buffer is sent to the screen later (when it’s full, or when the program finishes, or when a newline \n is printed).
            # By setting flush=True, you force Python to immediately flush the buffer — i.e., send the output to the terminal right away.
            # flush=True ensures real-time output, which is very important in streaming scenarios (like OpenAI SDK events).
            
            # print(event.data) # It will show data instance of ResponseTextDeltaEvent class
    
if __name__ == "__main__":
    asyncio.run(main())