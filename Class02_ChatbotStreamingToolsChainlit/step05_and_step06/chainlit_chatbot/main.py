import os
import chainlit as cl
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Step 1: Provider Setup
# Initialize the OpenAI provider with the Gemini API key
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Step 2: Model Setup
# Initialize the OpenAI chat completions model with the provider
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider,
)

# Step 3: Configure the agent at 'run' level
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True,
)

# Step 4: Create the instance of the agent
agent = Agent(
    name="GeminiAgent",
    instructions="You are a helpful assistant that provides information based on user queries.",
)

# Step 5: Create the runner instance
# This step is outside the chainlit when you are making just agent without any chainlit UI

# result = Runner.run_sync(
#     run_config=config,
#     input="What is the capital of France?",
#     # You can also write just agent on first line in Runner.run_sync b/c it is positional argument
#     # but here we are using named argument for clarity
#     starting_agent=agent,
# )

# print(result)  # Output the result of the agent's response

# To make it statefull (not stateless) and use chainlit UI, we need to use the `@cl.on_chat_start` decorator to manage the history of messages

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Hello! I am your support agent. How can I assist you today?"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")

    history.append({
        "role": "user",
        "content": message.content,
    })

    result = await Runner.run(
        agent,
        run_config=config,
        input=history,
    )

    history.append({
        "role": "assistant",
        "content": result.final_output,
    })

    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()