from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def app():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    agent = Agent(
        task="Search Youtube for videos on the OpenAI SDK and recommend the best one based on relevance, views and quality. Provide the video's title, channel, URL and 100 words summary of its content, highlighting key points and why it's best? Dont play any video.",
        llm=llm,
    )

    await agent.run()

asyncio.run(app())