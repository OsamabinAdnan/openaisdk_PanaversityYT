from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
import asyncio
from dotenv import load_dotenv
import chainlit as cl
import time

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = AsyncOpenAI(
    api_key= gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

config = RunConfig(
    model=model,
    model_provider= client,
    tracing_disabled=True,
)

frontend_expert_agent = Agent(
    name="Frontend Expert Developer",
    instructions="You are a frontend expert developer, your job is to create the frontend of the application according to the requirements provided by the user. You are expert in making frontend applications using React, Angular, Next.js and Vue.js. You will also be responsible for creating the user interface and user experience of the application.",
)

backend_expert_agent = Agent(
    name="Backend Expert Developer",
    instructions="You are a backend expert developer, your job is to create the backend of the application according to the requirements provided by the user. You are expert in making backend applications using Node.js, Python, Ruby on Rails and Java. You will also be responsible for creating the APIs and database of the application.",
)

animation_expert_agent = Agent(
    name="Animation Expert Developer",
    instructions="You are an animation expert developer, your job is to create the animations for the application according to the requirements provided by the user. You are expert in making animations using CSS, JavaScript, Framer Motion, Three.js and libraries like GSAP and Anime.js. You will also be responsible for creating the user interface and user experience of the application with animations.",
)

SEO_expert_agent = Agent(
    name="SEO Expert Developer",
    instructions="You are an SEO expert developer, your job is to optimize the application for search engines according to the requirements provided by the user. You are expert in making applications SEO friendly using techniques like keyword optimization, meta tags, structured data, and other SEO best practices. You will also be responsible for ensuring that the application is easily discoverable by search engines and ranks well in search results.",
)

manager_agent = Agent(
    name="Manager Agent",
    instructions="You are manager agent, you job is to manage the frontend expert developer agent, backend expert developer agents, animation_expert_agent and SEO_expert_agent. You will be responsible for assigning tasks to the agents and delegate work according to their expertise. You will also be responsible for coordinating the work between these agents and ensuring that the final output is cohesive and meets the requirements of the user.",
    tools = [
        frontend_expert_agent.as_tool(
            tool_name="frontend_expert",
            tool_description="Frontend Expert Developer Agent. You will be responsible for creating the frontend of the application according to the requirements provided by the user. You are expert in making frontend applications using React, Angular, Next.js and Vue.js. You will also be responsible for creating the user interface and user experience of the application.",
        ),
        backend_expert_agent.as_tool(
            tool_name="backend_expert",
            tool_description="Backend Expert Developer Agent. You will be responsible for creating the backend of the application according to the requirements provided by the user. You are expert in making backend applications using Node.js, Python, Ruby on Rails and Java. You will also be responsible for creating the APIs and database of the application.",
        ),
        animation_expert_agent.as_tool(
            tool_name="animation_expert",
            tool_description="Animation Expert Developer Agent. You will be responsible for creating the animations for the application according to the requirements provided by the user. You are expert in making animations using CSS, JavaScript, Framer Motion, Three.js and libraries like GSAP and Anime.js. You will also be responsible for creating the user interface and user experience of the application with animations.",
        ),
        SEO_expert_agent.as_tool(
            tool_name="SEO_expert",
            tool_description="SEO Expert Developer Agent. You will be responsible for optimizing the application for search engines according to the requirements provided by the user. You are expert in making applications SEO friendly using techniques like keyword optimization, meta tags, structured data, and other SEO best practices. You will also be responsible for ensuring that the application is easily discoverable by search engines and ranks well in search results.",
        ),
    ]
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="Hi! I am Osama bin Adnan's assistant, I have expertise in frontend, backend, animation and SEO development. How can I help you today.").send()
    cl.user_session.set("history", [])

@cl.on_message
async def handle_message(message:cl.Message):
    await cl.Message(content="Thinking...").send()
    history = cl.user_session.get("history", [])
    history.append(
        {
            "role":"user",
            "content": message.content,
        }
    )
    result = await Runner.run(
        manager_agent,
        input=history,
        run_config=config,
    )

    history.append(
        {
            "role": "assistant",
            "content": result.final_output,
        }
    )
    cl.user_session.set("history", history)
    await cl.Message(
        content=result.final_output,
    ).send()