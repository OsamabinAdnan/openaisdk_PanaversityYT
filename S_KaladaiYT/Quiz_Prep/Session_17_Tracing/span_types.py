from dotenv import load_dotenv
from agents import Agent, Runner, Trace, trace, function_tool, set_tracing_export_api_key, OpenAIChatCompletionsModel, set_trace_processors, set_tracing_disabled
from openai import AsyncOpenAI
from rich import print
import os
from agents.tracing.processors import BatchTraceProcessor, ConsoleSpanExporter,  default_processor

load_dotenv()

# from agents.tracing.processor_interface import TracingExporter

# #  STEP 1: Enable tracing
# set_tracing_disabled(disabled=True)  


#  STEP 2: Setup your custom exporter/processor
exporter = ConsoleSpanExporter()  # or use BackendSpanExporter()
processor = BatchTraceProcessor(exporter)
set_trace_processors(
    [processor, default_processor()] # sent to the dashbaord openai
)  # override default processor(s)


tracking_api_key = os.environ["OPENAI_API_KEY"]
set_tracing_export_api_key(tracking_api_key)

MODEL_NAME = "gemini-2.5-flash" # which LLM model will agent use

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY is not set")

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise Exception("BASE_URL is not set")


# external_client is the connection that allows us to talk with Gemini API
external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY,
        base_url = BASE_URL, #it is Gemini api endpoint bcx we are using Gemini LLM in OpenAI Agents framework
)

model = OpenAIChatCompletionsModel(
        model = MODEL_NAME,
        openai_client=external_client, #connect external cient with OpenAI client
)


@function_tool
def get_weather(city: str) -> str:
    """Get the current weather of a city."""
    return f"The weather in {city} is sunny around 33 C"



main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model=model,
    tools=[get_weather]
)

with trace(workflow_name="weather_forecast"):
    result= Runner.run_sync(
    main_agent,
    "What is the current weather in New York?"
    )

    print(result.final_output)
