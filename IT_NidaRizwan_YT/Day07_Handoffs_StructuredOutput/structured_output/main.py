
from dotenv import load_dotenv
import os
import asyncio
from agents import (
    Agent, 
    Runner, 
    OpenAIChatCompletionsModel, 
    set_tracing_disabled, 
    RunConfig,
    function_tool
)
from openai import AsyncOpenAI
from pydantic import BaseModel
import requests

load_dotenv()
set_tracing_disabled(True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")

weather_api_key = os.getenv("WEATHER_API_KEY")
if not weather_api_key:
    raise Exception("Missing WEATHER_API_KEY environment variable")

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# External Client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

@function_tool
def get_weather(city:str) -> str:
    """Get the weather in a city"""
    print(f"Calling Tool: get_weather({city})")
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}")
    data = response.json()
    return f"The weather in {city} is {data['current']['condition']['text']} and temperature is {data["current"]["temp_c"]} C, as of {data["current"]["last_updated"]}"

class WeatherAnswer(BaseModel):
    location: str
    temperature_c: float
    summary: str

async def main():

    agent = Agent(
        name= "Structured Weather Agent",
        instructions="Get the weather in a city from the get_weather tool then use the final_output tool with WeatherAnswer schema.",
        tools=[get_weather],
        output_type=WeatherAnswer,
        model=model,
    )

    result = await Runner.run(
        agent,
        input="What is the weather in Karachi?",
        run_config=config
    )
    print("\nAgent Output\n")
    print(type(result.final_output))
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())