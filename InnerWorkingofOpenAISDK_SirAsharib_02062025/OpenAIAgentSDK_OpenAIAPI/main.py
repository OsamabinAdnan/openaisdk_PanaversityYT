from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

# making instance of Agent class which is greeting_agent
greeting_agent = Agent(
    name= "Greeting Agent",
    instructions= "You are a greeting agent. Your task is to say salam when someone says hello, hi or anything like that.",
    # model= by default it uses GPT-4o
    handoffs= [], # handoffs are used to pass the output of one agent to another, they are empty list usually if no handoff is needed
    tools= [], # tools are used to perform actions, they are empty list usually if no tool is needed
)

# making instance of Runner class which is greeting_runner
agent_result = Runner.run_sync(
    greeting_agent,
    input= "Hello, what's up?",
)

print(agent_result.final_output)