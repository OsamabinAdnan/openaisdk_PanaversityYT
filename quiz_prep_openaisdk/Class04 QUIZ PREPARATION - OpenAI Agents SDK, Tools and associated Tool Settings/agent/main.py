import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, ModelSettings
from openai import AsyncOpenAI
from agents.agent import StopAtTools

load_dotenv()

set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

@function_tool()
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers together."""
    print("Tool called")
    return a + b - 2.5

@function_tool()
def human_review():
    """Human in the loop interface."""
    print("Human review requested")
    return "Human review completed."

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

agent = Agent(
    name="Gemini Agent",
    instructions="You are a helpful assistant that can answer questions and provide information.",
    model=model,
    tools=[add_numbers, human_review],
    # tool_use_behavior="stop_on_first_tool", # Stop after the first tool is used, by default it set as 'run_llm_again'
    # tool_use_behavior=StopAtTools(stop_on_first_tool=['human_review']),
    model_settings=ModelSettings(tool_choice="required"),
    reset_tool_choice=False,
    
)

# print(agent.tools)

result = Runner.run_sync(
    agent,
    input="Hello, What is the sum of 5 and 10? after result, ask the human to review.",
    context=None,
    max_turns=5, # Maximum number of turns to run the agent
)

print("Agent Response:", result.final_output)

