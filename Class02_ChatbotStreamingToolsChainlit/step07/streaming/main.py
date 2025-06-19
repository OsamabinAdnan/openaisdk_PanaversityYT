import os
import chainlit as cl
from agents import Agent, RunConfig, OpenAIChatCompletionsModel,AsyncOpenAI, Runner
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Step 01: Provider setup
# Initialize the OpenAI provider with the Gemini API key
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Step 02: Model setup
# Initialize the OpenAI chat completions model with the provider
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Step 03: Configure the agent at `run` level
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

# Step 04: Create the agent instance
agent = Agent(
    name="Panaversity Suppport Agent",
    instructions="You are a helpful assistant that can answer all questions",
)

# Step 05: Create the runner instance
# This step is outside the chainlit when you are making just agent without any chainlit UI

# result = Runner.run_sync(
#     run_config=config,
#     input="What is the capital of France?",
#     # You can also write just agent on first line in Runner.run_sync because it is positional argument
#     # but here we are using named argument for clarity
#     starting_agent=agent, # You can also pass a list of agents here in case of multi-agent setups
# )

# print(result.final_output)

# To make it statefull (not stateless) and use Chainlit UI, we need to use the `@cl.on_chat_start` decorator to manage the history of messages
@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Hello! I am your support agent. How can I assist you today?"
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    msg = cl.Message(
        content = "",
    )
    await msg.send()



    history.append({
        "role": "user",
        "content": message.content,
    })
    result = Runner.run_streamed(
        agent,
        input=history,
        run_config=config,
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await msg.stream_token(event.data.delta)

    history.append({
        "role": "assistant",
        "content": result.final_output,
    })
    cl.user_session.set("history", history)
    # await cl.Message(content=result.final_output).send()