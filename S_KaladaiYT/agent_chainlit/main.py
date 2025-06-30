from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
import asyncio
from dotenv import load_dotenv
import chainlit as cl
import time

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

config = RunConfig(
    model=model,
    model_provider= client,
    tracing_disabled=True,
)

agent = Agent(
    name="Frontend Expert Developer",
    instructions="A frontend expert developer with extensive knowledge in React, Vue, Nextjs and Angular.",
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Welcome to the Frontend Expert Developer chat!").send()
    cl.user_session.set("history", [])

@cl.on_message
async def handle_message(message:cl.Message):
    await cl.Message(content="Thinking...").send()
    history = cl.user_session.get("history", [])
    history.append(
        {
            "role":"user",
            "content": message.content,
        }
    )
    result = await Runner.run(
        agent,
        input=history,
        run_config=config,
    )

    history.append(
        {
            "role": "assistant",
            "content": result.final_output,
        }
    )
    cl.user_session.set("history", history)
    await cl.Message(
        content=result.final_output,
    ).send()