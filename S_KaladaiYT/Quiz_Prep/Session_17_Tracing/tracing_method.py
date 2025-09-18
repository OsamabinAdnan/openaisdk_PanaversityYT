from dotenv import load_dotenv
from agents import Agent, Runner, Trace, custom_span, function_tool, trace, Span, ModelSettings
from rich import print

load_dotenv()

@function_tool
def get_weather(city: str) -> str:
    """Get the current weather of a city."""
    return f"The weather in {city} is sunny around 33 C"


main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model="gpt-4o-mini",
    tools=[get_weather],
)

t = trace(workflow_name="weather_prediction")
# t.export()
t.start(mark_as_current=True)
print("Trace started")
print(t.trace_id)

# s = custom_span(name="weather_span")
# print("Span started")
# print(s.span_id)

result= Runner.run_sync(
main_agent,
"What is the weather in Karachi?"
)

print(result.final_output)


t.finish(reset_current=False) # By default is False, if True then it will reset the current trace

result2= Runner.run_sync(
main_agent,
"What is the population of Karachi in 2 lines?"
)

print(result2.final_output)