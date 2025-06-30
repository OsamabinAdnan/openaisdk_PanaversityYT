# Import necessary modules and classes
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
import asyncio
from dotenv import load_dotenv
import chainlit as cl
import time

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
# Raise an error if not set
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

# Initialize the OpenAI client with Gemini API key and base URL
client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Set up the model configuration
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client,
)

# Configure the run settings for the agent runner
config = RunConfig(
    model=model,
    model_provider= client,
    tracing_disabled=True,
)

# Define the Frontend Expert Agent
frontend_expert_agent = Agent(
    name="Frontend Expert Developer",
    instructions="You are a frontend expert developer, your job is to create the frontend of the application according to the requirements provided by the user. You are expert in making frontend applications using React, Angular, Next.js and Vue.js. You will also be responsible for creating the user interface and user experience of the application.",
    handoff_description="You will be responsible for creating the frontend of the application according to the requirements provided by the user. You are expert in making frontend applications using React, Angular, Next.js and Vue.js. You will also be responsible for creating the user interface and user experience of the application.",
)

# Define the Backend Expert Agent
backend_expert_agent = Agent(
    name="Backend Expert Developer",
    instructions="You are a backend expert developer, your job is to create the backend of the application according to the requirements provided by the user. You are expert in making backend applications using Node.js, Python, Ruby on Rails and Java. You will also be responsible for creating the APIs and database of the application.",
    handoff_description="You will be responsible for creating the backend of the application according to the requirements provided by the user. You are expert in making backend applications using Node.js, Python, Ruby on Rails and Java. You will also be responsible for creating the APIs and database of the application.",
)

# Define the Animation Expert Agent
animation_expert_agent = Agent(
    name="Animation Expert Developer",
    instructions="You are an animation expert developer, your job is to create the animations for the application according to the requirements provided by the user. You are expert in making animations using CSS, JavaScript, Framer Motion, Three.js and libraries like GSAP and Anime.js. You will also be responsible for creating the user interface and user experience of the application with animations.",
    handoff_description="You will be responsible for creating the animations for the application according to the requirements provided by the user. You are expert in making animations using CSS, JavaScript, Framer Motion, Three.js and libraries like GSAP and Anime.js. You will also be responsible for creating the user interface and user experience of the application with animations.",
)

# Define the SEO Expert Agent
SEO_expert_agent = Agent(
    name="SEO Expert Developer",
    instructions="You are an SEO expert developer, your job is to optimize the application for search engines according to the requirements provided by the user. You are expert in making applications SEO friendly using techniques like keyword optimization, meta tags, structured data, and other SEO best practices. You will also be responsible for ensuring that the application is easily discoverable by search engines and ranks well in search results.",
    handoff_description="You will be responsible for optimizing the application for search engines according to the requirements provided by the user. You are expert in making applications SEO friendly using techniques like keyword optimization, meta tags, structured data, and other SEO best practices. You will also be responsible for ensuring that the application is easily discoverable by search engines and ranks well in search results.",
)

# Define the Manager Agent, which manages all other agents and delegates tasks
manager_agent = Agent(
    name="Manager Agent",
    instructions="""
        You are a manager agent. Your job is to:
        - Receive user requests and analyze which expert agent (frontend, backend, animation, SEO) is best suited for each part of the request.
        - Delegate each task to the appropriate expert agent using their tool.
        - If the user asks for code or a specific technology, explicitly instruct the relevant agent to generate code as per the user's requirements.
        - Collect responses from the expert agents and combine them into a single, cohesive reply for the user.
        - You do NOT write code yourself. You only coordinate and delegate.
        - Always ensure that if the user requests code, the code is delivered back from the appropriate agent.
        - If an agent does not return a response, retry or inform the user of the issue.
    """,
    handoffs = [frontend_expert_agent, backend_expert_agent, animation_expert_agent, SEO_expert_agent],
)

# Event handler for chat start: sends a welcome message and initializes user session history
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Hi! I am Osama bin Adnan's assistant, I have expertise in frontend, backend, animation and SEO development. How can I help you today.").send()
    cl.user_session.set("history", [])

# Event handler for incoming messages: processes user input and generates a response
@cl.on_message
async def handle_message(message:cl.Message):
    # Create a reply message
    reply = await cl.Message(content="⏳ Thinking...").send()
    # Retrieve conversation history from user session
    history = cl.user_session.get("history", [])
    # Add user message to history
    history.append(
        {
            "role":"user",
            "content": message.content,
        }
    )
    # Run the manager agent with the conversation history
    result = await Runner.run(
        manager_agent,
        input=history,
        run_config=config,
    )

    # Add assistant's response to history
    history.append(
        {
            "role": "assistant",
            "content": result.final_output,
        }
    )
    cl.user_session.set("history", history)

    # Send the assistant's response to the user
    # Update the reply message with the final output
    reply.content = result.final_output
    # Update the reply message in the chat
    await reply.update()