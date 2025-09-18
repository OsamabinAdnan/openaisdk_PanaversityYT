from dotenv import load_dotenv
from agents import Agent, Runner, Trace, trace
from rich import print

load_dotenv()

main_agent = Agent(
    name="Assistant",
    instructions="You are helpful assistant",
    model="gpt-4o-mini"
)

with trace(
    workflow_name="OBA89",
    
    # trace_id="trace_id_12345", 
    
    group_id="group_id_12345", 
    # Optional grouping identifier to link multiple traces from the same conversation or process. For instance, you might use a chat thread ID | Used when you want to correlate or analyze many traces together (e.g. all traces for a particular user, session, A/B test bucket, or experiment).| Not automatically generated — you set it yourself when running.

    # metadata={"name": "OBA89"},

    disabled=False
    # By default False, if True, we will return a Trace but the Trace will not be recorded.
):
    result= Runner.run_sync(
    main_agent,
    "What is Agentic AI in 2 lines?"
    )

    print(result.final_output)

    # # Below code is used to understand group_id
    # result2 = Runner.run_sync(
    # main_agent,
    # "What is Machine Learning in 2 lines?"
    # )

    # print(f"\n{result2.final_output}")