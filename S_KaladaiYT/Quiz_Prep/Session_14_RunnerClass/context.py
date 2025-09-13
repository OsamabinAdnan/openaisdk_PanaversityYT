from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, RunContextWrapper, function_tool, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from rich import print
from dataclasses import dataclass


load_dotenv()

enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model_25 = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

model_20 = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=my_client,
)

# Class to make context
@dataclass
class BankContext:
    account_data : dict | None = None

account_database = {
    "1234" : {
        "name" : "John Doe",
        "balance" : 1000
    },
    "5678" : {
        "name" : "Jane Doe",
        "balance" : 2000
    },
    "9012" : {
        "name" : "Bob Smith",
        "balance" : 3000
    }
}

@function_tool
async def check_balance(ctx:RunContextWrapper[BankContext], account_number:str) -> str:
    """
    Check account balance for giving account number
    """
    my_ctx = ctx.context # my_ctx is the whole BankContext object.
    account_info = my_ctx.account_data.get(account_number) # You then access .account_data from it and do .get(account_number).
    if account_info:
        return f"Account holder name: {account_info['name']}, Account balance: PKR {account_info['balance']}"
    else:
        return f"Account number: {account_number} not found"



bank_context = BankContext(
    account_data=account_database
)

main_agent = Agent(
    name="Main Agent",
    instructions="""
        You are helpful assistant.
    """,
    model=model_25,
    tools=[check_balance],
)

result = Runner.run_sync(
    main_agent,
    "Hello! What is current balance of account number 1234?",
    context=bank_context,
)

print(f"\n{result.final_output}\n")
