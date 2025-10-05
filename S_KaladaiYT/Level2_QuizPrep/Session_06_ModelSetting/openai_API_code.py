from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings
from rich import print

load_dotenv()

setting = ModelSettings(
    top_p= 0.5 # Range from 0.0 to 1.0
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-3.5-turbo",
    model_settings=setting,
)

result = Runner.run_sync(agent, "What is Agentic AI? explaine in 3 lines.")

print(f"\nTop_p: {agent.model_settings.top_p}")
print("=" * 30)
print(f"Agent Response:")
print("=" * 30)
print(f"\n{result.final_output}\n")