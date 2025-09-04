import os
from dotenv import load_dotenv
from agents import Agent, Runner, FileSearchTool, CodeInterpreterTool

load_dotenv()

FILE_ID = os.getenv("FILE_ID")
if not FILE_ID:
    raise ValueError("FILE_ID is not set")

agent = Agent(
    name="Code_Interpreter_Agent",
    instructions="You are a helpful assistant.",
    model="gpt-4o",
    tools = [CodeInterpreterTool(
        tool_config={
            "type": "code_interpreter",
            "container": {
                "type": "auto",
                "file_ids":[FILE_ID]
            }
        }
    )] 
)

result = Runner.run_sync(
    agent,
    "Who is Osama bin Adnan? Give me a short bio.",
)

print(result.final_output)