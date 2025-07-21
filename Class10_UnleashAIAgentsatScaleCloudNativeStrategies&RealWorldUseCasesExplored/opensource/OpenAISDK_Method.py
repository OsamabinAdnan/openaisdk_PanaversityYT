import os
from openai import AsyncOpenAI  # Async OpenAI client for API communication
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled  # Custom agents framework
from dotenv import load_dotenv  # For loading environment variables from .env file
import asyncio  # For running asynchronous code

# Load environment variables from a .env file
load_dotenv()

# Disable tracing (useful if you don’t want logs sent to external tracing services)
set_tracing_disabled(True)

# Retrieve the OpenRouter API key from environment variables
OpenRouter_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OpenRouter_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

# Set base URL and model name for OpenRouter
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "deepseek/deepseek-r1-0528-qwen3-8b:free"

# Note: You can explore available free models at:
# https://openrouter.ai/models?fmt=table&max_price=0

# Create an asynchronous OpenAI client configured to talk to OpenRouter
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=OpenRouter_API_KEY,
)

# Initialize the model using the custom agent-compatible wrapper
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=client,
)

# Define the main async function
async def main():
    # Set up the agent with instructions to reply only in haiku format
    agent = Agent(
        name="Assitant",  # You can name the agent anything
        instructions="You only respond in haiku format.",
        model=model,  # Assign the previously initialized model
    )

    # Run the agent with a given prompt
    result = await Runner.run(
        agent,
        "Write a haiku about the beauty of nature.",  # Prompt passed to the agent
    )

    # Print the final response from the agent
    print("\nResponse from OpenRouter API:\n")
    print(result.final_output)

# Run the asynchronous main function if this file is executed directly
if __name__ == "__main__":
    asyncio.run(main())
