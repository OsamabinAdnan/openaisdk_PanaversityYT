import os
from dotenv import load_dotenv
from agents import Agent, Runner, FileSearchTool

load_dotenv()

VECTOR_DATABASE_ID = os.getenv("VECTOR_DATABASE_ID")
if not VECTOR_DATABASE_ID:
    raise ValueError("VECTOR_DATABASE_ID is not set")

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
    tools = [FileSearchTool(
        vector_store_ids=[VECTOR_DATABASE_ID],
    )]
)

result = Runner.run_sync(
    agent,
    "Who is Osama bin Adnan? Give me a short bio.",
)

print(result.final_output)