import asyncio
import uuid
import os
from dotenv import load_dotenv
from rich import print
from agents import Agent, Runner, OpenAIChatCompletionsModel, RawResponsesStreamEvent, TResponseInputItem, trace, enable_verbose_stdout_logging
from openai.types.responses import ResponseContentPartDoneEvent, ResponseTextDeltaEvent
from openai import AsyncOpenAI



load_dotenv()

# enable_verbose_stdout_logging()
"""
This example shows the handoffs/routing pattern. The triage agent receives the first message, and
then hands off to the appropriate agent based on the language of the request. Responses are
streamed to the user.
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

french_agent = Agent(
    name="french_agent",
    instructions="You only speak French",
    model=llm_model,
)

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You only speak Spanish",
    model=llm_model,
)

english_agent = Agent(
    name="english_agent",
    instructions="You only speak English",
    model=llm_model,
)

french_agent.handoffs = [spanish_agent, english_agent]
spanish_agent.handoffs = [french_agent, english_agent]
english_agent.handoffs = [french_agent, spanish_agent]


triage_agent = Agent(
    name="triage_agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[french_agent, spanish_agent, english_agent],
    model=llm_model,
)


async def main():
    # We'll create an ID for this conversation, so we can link each trace
    conversation_id = str(uuid.uuid4().hex[:16])

    msg = input("Hi! We speak French, Spanish and English. How can I help? ")
    agent = triage_agent
    inputs:list[TResponseInputItem] = [
        {
            "role": "user",
            "content": msg,
        }
    ]

    while True:
        # Each conversation turn is a single trace. Normally, each input from the user would be an
        # API request to your app, and you can wrap the request in a trace()

        with trace (workflow_name="Routing example", group_id=conversation_id):
            result = Runner.run_streamed(
                starting_agent=agent,
                input=inputs,
            )

            async for event in result.stream_events():
                if not isinstance(event, RawResponsesStreamEvent):
                    continue
                data = event.data
                if isinstance(data, ResponseTextDeltaEvent):
                    print(data.delta, end="", flush=True)
                elif isinstance(data, ResponseContentPartDoneEvent):
                    print('\n')
        

        inputs = result.to_input_list()
        print('\n')

        user_msg = input("Enter a message: ")
        print(f"Current Agent: {result.current_agent.name}")
        inputs.append({"content": user_msg, "role": "user"})
        agent = result.current_agent

if __name__ == "__main__":
    asyncio.run(main())

