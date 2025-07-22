# Importing required classes and functions from custom agent framework and external libraries
from agents import (
    Agent,                          # Represents an AI agent with specific instructions and capabilities
    Runner,                         # Used to run agents
    OpenAIChatCompletionsModel,     # Wrapper for OpenAI-compatible chat models
    set_tracing_disabled,           # Disables tracing/logging for agent runs
    input_guardrail,                # Decorator to apply input guardrails
    RunContextWrapper,              # Wrapper for managing execution context
    TResponseInputItem,             # Typing for individual input item (used with lists)
    GuardrailFunctionOutput,        # Output format for guardrail functions
    InputGuardrailTripwireTriggered, # Exception raised when guardrail is triggered
    output_guardrail,               # Decorator to apply output guardrails
    OutputGuardrailTripwireTriggered, # Exception raised when output guardrail is triggered
)

from openai import AsyncOpenAI         # Async OpenAI-compatible client
from dotenv import load_dotenv         # Loads environment variables from a .env file
from pydantic import BaseModel         # Base class for data validation and modeling
import os                              # Provides access to environment variables
import chainlit as cl                  # Chainlit framework for building chat UIs

# Load environment variables from .env file
load_dotenv()

# Disable tracing for agent executions (optional, usually for privacy/debugging)
set_tracing_disabled(True)

# Define base URL for OpenAI-compatible API endpoint (in this case, Gemini)
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Define the model name to use from Gemini API
MODEL = "gemini-2.0-flash"

# Retrieve API key for Gemini model from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")  # Raise error if key not found

# Initialize OpenAI-compatible async client with Gemini base URL and API key
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=gemini_api_key,
)

# Create a chat model instance using the Gemini model and client
model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client,
)

# @@@@@@@@@@@@@@@ Input guardrail @@@@@@@@@@@@@@@@

# Define the expected output format for the guardrail check using Pydantic
class OutputPythonType(BaseModel):
    is_python_related: bool   # Whether the input is related to Python
    reasoning: str            # Reasoning behind the classification decision

# Define a dedicated agent to check if input is appropriate for Python programming
input_guardrails_agent = Agent(
    name="Input Guardrails Checker",     # Name of the agent
    instructions="""                     # Instructions that guide the behavior of the agent
    - You are an input guardrails checker. Your task is to determine if the input is appropriate with python programming.
    - If the input is not appropriate, respond with a message indicating that the input is not suitable for Python programming and end the conversation.
    - If the input is appropriate, respond with a message indicating that the input is suitable for Python programming and continue the conversation.
    """,
    model=model,                         # Use the Gemini chat model
    output_type=OutputPythonType,        # Output must match this Pydantic structure
)

# Define a function that wraps guardrail logic using a decorator
@input_guardrail
async def input_guardrail_function(
    context: RunContextWrapper,               # Execution context wrapper
    agent: Agent,                             # Agent instance passed automatically
    input: str | list[TResponseInputItem],    # Input string or list of structured input items
) -> GuardrailFunctionOutput:                 # Returns structured output including tripwire status

    # Run the input against the guardrail agent
    result = await Runner.run(
        input_guardrails_agent,
        input,
    )

    # Return whether a guardrail was triggered based on the agent’s classification
    return GuardrailFunctionOutput(
        output_info=result.final_output,                           # Agent's full output
        tripwire_triggered=not result.final_output.is_python_related,  # Trigger tripwire if not Python-related
    )

# @@@@@@@@@@@@@@@ Output guardrail @@@@@@@@@@@@@@@@
class MessageOutput(BaseModel):
    response:str # Response message to be sent back to the user

class PythonOutput(BaseModel):
    is_python: bool          # Indicates if the input is Python-related
    reasoning: str           # Reasoning for the classification

output_guardrail_agent = Agent(
    name="Output Guardrails Checker",  # Name of the output guardrail agent
    instructions="""                  # Instructions for the output guardrail agent
    - You are an output guardrails checker. Your task is to determine if the output is appropriate for Python programming and output related to python related.
    - If the output is not appropriate, respond with a message indicating that the output is not suitable for Python programming and end the conversation.
    - If the output is appropriate, respond with a message indicating that the output is suitable for Python programming and continue the conversation.
    """,
    output_type=PythonOutput,  # Expected output type for the agent
    model=model,                # Use the Gemini chat model
)

@output_guardrail
async def output_guardrail_function(
    context: RunContextWrapper[None], # Execution context wrapper (not used here)
    agent: Agent,                     # Agent instance passed automatically
    output: MessageOutput,            # Output message or structured output
) -> GuardrailFunctionOutput:         # Returns structured output including tripwire status
    output_result = await Runner.run(
        output_guardrail_agent,
        output,
    )

    return GuardrailFunctionOutput(
        output_info= output_result.final_output,  # Full output from the agent
        tripwire_triggered= not output_result.final_output.is_python,  # Trigger tripwire if not Python-related
    )


# @@@@@@@@@@@@@@@@@ Main Agent @@@@@@@@@@@@@@@@@

# Define the main AI agent to answer Python-related questions
main_agent = Agent(
    name="Python Expert Agent",     # Name of the expert agent
    instructions=" Give a warmth answer to the user's hi and hello. You are a Python expert agent. Your task is to provide accurate and helpful responses to Python-related queries.",  # Agent instructions
    model=model,                    # Gemini model used for this agent
    input_guardrails=[input_guardrail_function],  # Guardrail applied to incoming user inputs
    output_guardrails=[output_guardrail_function],  # Guardrail applied to outgoing responses
)

# Event triggered when a new chat session starts
@cl.on_chat_start
async def on_chat_start():
    # Send a welcome message to the user
    await cl.Message(
        content="Welcome to the Python Expert Agent! You can ask me anything related to Python programming."
    ).send()

# Event triggered when a message is received from the user
@cl.on_message
async def on_message(message: cl.Message):
    try:
        # Pass the user's input to the main agent for processing
        result = await Runner.run(
            main_agent,
            input=message.content,
        )
        # Send the agent's response back to the user
        await cl.Message(content=result.final_output).send()

    # Handle case where guardrail is triggered (non-Python input)
    except InputGuardrailTripwireTriggered as e:
        await cl.Message(
            content="🛑 Your query is not suitable for Python programming. Please provide a valid Python-related query."
        ).send()
    
    except OutputGuardrailTripwireTriggered as e:
        await cl.Message(
            content="🛑 The output is not suitable for Python programming. Please provide a valid Python-related query."
        ).send()

