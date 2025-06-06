# Import required libraries
# Agent class is used to create an AI agent with specific capabilities
# Runner class is used to execute the agent and get results
from agents import Agent, Runner
# Load environment variables from .env file
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

# Create an instance of the Agent class for handling greetings
# This agent is specifically designed to respond to greeting messages
greeting_agent = Agent(
    name= "Greeting Agent",
    instructions= "You are a greeting agent. Your task is to say salam when someone says hello, hi or anything like that.",
    # By default, the agent uses GPT-4 model
    # handoffs parameter allows passing output between multiple agents (empty if not needed)
    handoffs= [], 
    # tools parameter defines any special capabilities the agent might need (empty if no special tools required)
    tools= [],
    # model parameter allows specifying a different model for the agent
    model= "gpt-4.1"
)

# Get user input from console
user_input = input("Enter your query here:")

# Execute the agent with the user's input
# Runner.run_sync runs the agent synchronously and waits for the response
agent_result = Runner.run_sync(
    greeting_agent,
    input= user_input,
)

# Display the agent's response to the user
print(agent_result.final_output)