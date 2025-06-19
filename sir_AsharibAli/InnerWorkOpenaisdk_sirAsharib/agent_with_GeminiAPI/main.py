# Standard library imports
import os

# Third-party imports
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig, function_tool

# Load environment variables from .env file (for API keys)
load_dotenv()

# Configure Gemini model settings
MODEL_NAME = "gemini-1.5-flash"  # Using Gemini 1.5 Flash model for better performance
MY_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

if not MY_GEMINI_API_KEY:
    raise ValueError("Check your .env file for GEMINI_API_KEY")
    
external_client = AsyncOpenAI(
    api_key=MY_GEMINI_API_KEY,
    base_url=BASE_URL
)

model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client= external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

# Define a tool to fetch Asharib's profile information
@function_tool("get_asharib_info")
def get_asharib_info():
    """
    Fetches Asharib Ali's profile information from his personal API endpoint.
    
    Returns:
        dict: JSON response containing Asharib's profile information including:
            - Personal details
            - Work experience
            - Education
            - Skills
            - Projects and achievements
    """
    try:
        response = requests.get("https://asharib.xyz/api/profile")
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except Exception as e:
        print(f"Error fetching profile data: {e}")
        return {
            "error": "Failed to fetch information",
            "message": str(e)
        }

# Initialize the greeting agent to handle welcome messages
greeting_agent = Agent(
    name="Greeting Agent",
    model=model,
    instructions="""
    You are a greeting agent responsible for providing warm welcomes.
    When users greet with hi, hello, etc., respond with 'Assalamu Alaikum' and a friendly message.
    Keep responses concise and warm.
    """,
)

# Initialize the Asharib info agent to handle queries about Asharib Ali
asharib_info_agent = Agent(
    name="Asharib Info Agent",
    model=model,
    instructions="""
    You are an assistant specialized in providing information about Asharib Ali.
    For ANY question about Asharib:
    1. FIRST call get_asharib_info() to fetch his latest profile
    2. Check if the response contains an error field
    3. If successful, provide relevant information from the profile
    4. If there's an error, explain the issue to the user
    
    The profile includes:
    - Personal details and background
    - Work experience and achievements
    - Education history
    - Skills and projects
    
    Always cite specific details from the profile and never make up information.
    """,
    tools=[get_asharib_info]
)

# Initialize the coordinator agent to manage routing between specialized agents
coordinator_agent = Agent(
    name="Coordinator Agent",
    model=model,
    instructions="""
    You are a routing/Coordinator agent responsible for directing queries to the appropriate specialized agent.
    
    Routing Rules:
    1. For questions about Asharib Ali, his background, work, or achievements -> route to 'Asharib Info Agent'
    2. For greetings (hi, hello, etc.) -> route to 'Greeting Agent'
    
    Analyze each query carefully to determine the user's intent and route accordingly.
    Ensure proper handling of tools and context when routing to specialized agents.
    """,
    handoffs=[greeting_agent, asharib_info_agent],
    tools=[get_asharib_info]  # Make tool available for proper routing
)

user_input = input("Enter your greeting:")
    
agent_result =  Runner.run_sync(
    coordinator_agent, 
    user_input, run_config=config
)

print(f"Agent Response: {agent_result.final_output}")


