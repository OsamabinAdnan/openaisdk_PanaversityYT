import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import chainlit as cl
from dotenv import load_dotenv
import asyncio

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

external_client= AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_client
)

config = RunConfig(
    model = model,
    model_provider = external_client,
    tracing_disabled = True
)

agent = Agent(
    name = "Assistant",
    instructions = "You are a helpful assistant",
    model = model
)

@cl.on_chat_start
async def start():
    await cl.Message("Hello, I am here to help, ask me anything!").send()

@cl.on_message
async def on_message(message:cl.Message):
    await cl.Message("Thinking...").send()
    result = Runner.run_sync(agent, message.content, run_config=config)
    await cl.Message(result.final_output).send()

if __name__ == "__main__":
    asyncio.run(on_message())
