from agents import Agent, RunContextWrapper, Runner, OpenAIChatCompletionsModel, RunConfig, enable_verbose_stdout_logging, FunctionTool, function_tool
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from rich import print

load_dotenv()

enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

base_url = os.getenv("BASE_URL")
if not base_url:
    raise ValueError("BASE_URL is not set in environment variables")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client = external_client
)

# Instead of using FunctionTool class, you can also use @function_tool decorator to make tool
# For function tool decorator,
    # - You dont need to write schema separately, it will be generated automatically from function signature
    # - You dont need to invoke tool separately, it will be invoked automatically
    # - We used FunctionTool class when we want to have more control over schema and invocation

def supporter(ctx:RunContextWrapper, exception:Exception):
    return "The current weather in New York is cloudy with a high of 75°F and a low of 60°F."

@function_tool(
        name_override="get_current_weather",
        description_override="weather tool to get current weather in a given location",
        docstring_style="google",
        use_docstring_info=True, # By default, it True, set to False if you dont want to send docstring info to tool schema
        failure_error_function=supporter,
        strict_mode=False, # By default is True, set to False if you dont want to use required property for default values, like city in this case is set to default to "Karachi" so it is not required in required field of schema
        is_enabled=True, # By default is True, set to False if you want to disable tool, it will not be give to LLMs
)
def weather(city: str = "Karachi"):
    """Get the current weather for a given location.
    Args:
        city (str): The city to get the weather for.
    Returns:
        str: The current weather for the given location.
    """
    # return f"The current weather in {city} is sunny"
    raise ValueError("Error aagaya hai 🛑")  # Simulate an error for demonstration

# Create an AI agent with basic instructions
agent: Agent = Agent(
    name="Assistant",
    instructions="You are a helpful weather assistant, entertain user queries politely.",
    model=model,
    tools=[weather],
)

# Run the agent synchronously with a test question
result = Runner.run_sync(
    agent,
    "Hello, What is the weather in New York?",
)

print("\nCALLING AGENT")
print("=" * 50)

print(result.final_output)