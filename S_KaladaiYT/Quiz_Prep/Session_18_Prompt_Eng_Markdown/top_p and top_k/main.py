import os
from dotenv import load_dotenv
from agents import Agent, Runner, ModelSettings, RunConfig

load_dotenv()

runConfig = RunConfig(
    model_settings=ModelSettings(
        top_p=0.3,
    )
)

runConfig2 = RunConfig(
    model_settings=ModelSettings(
        top_p=1.0,
    )
)

main_agent = Agent(
    name="main agent",
    instructions="You are a helpful assistant.",
    model="gpt-4o-mini",
)

result = Runner.run_sync(
    main_agent,
    "What is Sun? explain in 3 lines",
    run_config=runConfig,
)

print(f"When top_p is 0.3: {result.final_output}")

result2 = Runner.run_sync(
    main_agent,
    "What is Sun? explain in 3 lines",
    run_config=runConfig2,
)

print(f"When top_p is 0.9: {result2.final_output}")