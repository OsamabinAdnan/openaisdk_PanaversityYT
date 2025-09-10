import os
from dotenv import load_dotenv
from agents import Agent, Handoff, Runner, OpenAIChatCompletionsModel, enable_verbose_stdout_logging, handoff
from openai import AsyncOpenAI
from pydantic import BaseModel
from agents.extensions import handoff_filters

load_dotenv()
# enable_verbose_stdout_logging()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise Exception("GEMINI_API_KEY is not set")

my_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=my_client,
)

class My_Input_Type(BaseModel):
    reasoning:str

agent = Agent(
    name="Billing Support Agent",
    instructions="You take care issue respect to billing, payments and support",
    model=model,
    handoff_description="You are expert billing agent, if user ask about billing, payments or support, then delegate to this agent"
)



main_agent = Agent(
    name="Main Agent",
    instructions="You are the main agent which will answer user query, if speclize agent is available then delegate to it",
    model=model,
    handoffs=[handoff(agent=agent,tool_name_override="billing_support_agent", tool_description_override="You are expert billing agent, if user ask about billing, payments or support, then delegate to this agent", input_filter=handoff_filters.remove_all_tools)], 
)

result = Runner.run_sync(
    main_agent,
    "Hello, I want to know about billing?"
)

print(result.final_output)

