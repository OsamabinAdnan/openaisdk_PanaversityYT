# Import required libraries
import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, function_tool
import asyncio

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Define a mock weather function tool
@function_tool
async def getweather(city:str) -> str:
    """Mock function to get weather information for a given city"""
    return f"The weather in {city} is cloudy with a temperature of 25°C."


# Initialize OpenAI client with Gemini API configuration
external_client= AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Configure the language model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Set up run configuration for the agents
config= RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

# Define Spanish-speaking agent
spanish_agent = Agent(
    name="spanish_agent",
    instructions="You are a Spanish-speaking agent. Your task is to assist users in Spanish.",
    handoff_description="You will reply in Spanish and assist with any questions or tasks related to the Spanish language.",
)

# Define French-speaking agent
french_agent = Agent(
    name="french_agent",
    instructions="You are a French-speaking agent. Your task is to assist users in French.",
    handoff_description="You will reply in French and assist with any questions or tasks related to the French language.",
)

# Define triage agent that coordinates between language agents
triage_agent = Agent(
    name="triage_agent",
    instructions="You are a triage agent. Your task is to analyze the input and determine the appropriate action.",
    handoffs=[spanish_agent, french_agent],
    tools=[getweather]
)


# Main async function to run the agent system
async def main():
    # Execute the triage agent with a weather query in Spanish
    result = await Runner.run(triage_agent, "What is weather in Karachi? tell me in spanish", run_config=config)
    
    # Print the results
    print("=" * 40)
    print(f"Result: {result.final_output}")
    print("=" * 40)
    print(f"Last Agent: {result.last_agent.name}")
    print(f"Last Tool Call: {triage_agent.tools[0].name}")

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())