import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, set_tracing_disabled, RunConfig
from dotenv import load_dotenv
import asyncio
load_dotenv()

set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Define a mock weather function tool
@function_tool
async def getweather(city:str) -> str:
    """Mock function to get weather information for a given city"""
    return f"The weather in {city} is cloudy with a temperature of 25°C."

# Initialize OpenAI client with Gemini API configuration
client_external = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Configure the language model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client_external,
)

config = RunConfig(
    model=model,
    model_provider= client_external,
    tracing_disabled=True,
)

# Define Spanish-speaking agent
spanish_agent = Agent(
    name="spanish_agent",
    instructions="You are a Spanish-speaking agent. Your task is to assist users in Spanish.",
    # handoff_description="You will reply in Spanish and assist with any questions or tasks related to the Spanish language.", # When we used agent as a tool, we don't need this description
)

# Define French-speaking agent
french_agent = Agent(
    name="french_agent",
    instructions="You are a French-speaking agent. Your task is to assist users in French.",
    # handoff_description="You will reply in French and assist with any questions or tasks related to the French language.", # When we used agent as a tool, we don't need this description
)

# Define triage agent that coordinates between language agents
triage_agent = Agent(
    name="triage_agent",
    instructions = "You are a translation agent. You use the tools given to you to translate. If asked for multiple translations, you call the relevant tools.",
    # handoffs = [spanish_agent, french_agent],
    tools = [   
                # we make the agents as tools
                spanish_agent.as_tool(
                    tool_name="translate_to_spanish", # No space in tool name
                    tool_description="Translate the input to Spanish and assist with any questions or tasks related to the Spanish language.",
                ),
                french_agent.as_tool(
                    tool_name="translate_to_french", # No space in tool name
                    tool_description="Translate the input to French and assist with any questions or tasks related to the French language.",
                ),
            ],
)

# Main async function to run the agent system
async def main():
    result = await Runner.run(
        triage_agent,
        "'Hello, how are you?' Translate to French",
        run_config=config
    )

    # Print the results
    print("=" * 40)
    print(f"Result: {result.final_output}")
    print("=" * 40)
    print(f"Last Agent: {result.last_agent.name}")
    print(f"Last Tool Call: {triage_agent.tools[0].name}")
    print(f"Last Agent Call: {result.last_agent.name}")

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())