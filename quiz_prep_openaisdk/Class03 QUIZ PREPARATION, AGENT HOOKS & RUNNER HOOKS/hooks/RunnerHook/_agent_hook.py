# agent_hook.py

from typing import Any, Generic
from typing_extensions import TypeVar
from agents import Agent, AgentBase, RunContextWrapper, TContext, Tool, RunHooks, Runner
from pydantic import BaseModel


TAgent = TypeVar("TAgent", bound=AgentBase, default=AgentBase)

class AgentHooksBase(Generic[TContext, TAgent]):
    """A class that receives callbacks on various lifecycle events for a specific agent. You can
    set this on `agent.hooks` to receive events for that specific agent.

    Subclass and override the methods you need.
    """
    # on_start: Called before the agent is invoked. Called each time the running agent is changed to this agent.
    async def on_start(self, context: RunContextWrapper[TContext], agent: TAgent) -> None:
        """Called before the agent is invoked. Called each time the running agent is changed to this
        agent."""
        pass
    
    # on_end: Called when the agent produces a final output.
    async def on_end(
        self,
        context: RunContextWrapper[TContext],
        agent: TAgent,
        output: Any,
    ) -> None:
        """Called when the agent produces a final output."""
        pass
    
    # on_handoff: Called when the agent is being handed off to. The source is the agent that is handing off to this agent.
    async def on_handoff(
        self,
        context: RunContextWrapper[TContext],
        agent: TAgent,
        source: TAgent,
    ) -> None:
        """Called when the agent is being handed off to. The `source` is the agent that is handing
        off to this agent."""
        pass

    # on_tool_start: Called before a tool is invoked.
    async def on_tool_start(
        self,
        context: RunContextWrapper[TContext],
        agent: TAgent,
        tool: Tool,
    ) -> None:
        """Called before a tool is invoked."""
        pass

    # on_tool_end: Called after a tool is invoked.
    async def on_tool_end(
        self,
        context: RunContextWrapper[TContext],
        agent: TAgent,
        tool: Tool,
        result: str,
    ) -> None:
        """Called after a tool is invoked."""
        pass


AgentHooks = AgentHooksBase[TContext, Agent]
"""Agent hooks for `Agent`s."""

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Below is rough working @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


# How can i passed custom (run) hooks to the agent?

class MyTestData(BaseModel):
    """An example Pydantic model for custom data."""
    name: str
    age: int


class MyCustomRunHooks(RunHooks):
    def on_agent_start(self, context:RunContextWrapper[MyTestData], agent:Agent):
        print(f"Agent {agent.name} started with context: {context.data}")
    
    def on_agent_end(self, context, agent, output):
        print(f"Agent {agent.name} ended with output: {output.final_output}")

class MyCustomAgentHooks(AgentHooks):
    def on_start(self, context:RunContextWrapper[MyTestData], agent:Agent):
        print(f"Agent {agent.name} started with context: {context.data}")
    
    def on_end(self, context, agent, output):
        print(f"Agent {agent.name} ended with output: {output.final_output}")

def dynamic_instruction(context:MyTestData):
    return f"Hello {context.name}, you are {context.age} years old."

myAgent = Agent(
    name="Test_Agent",
    instructions=dynamic_instruction,
    agent_hooks=MyCustomAgentHooks(), # Agent hooks pass in agent class's instance
)

test_data = MyTestData(name="John Doe", age=30)

output = Runner.run_sync(
    myAgent,
    input="Hello, how are you?",
    hooks=MyCustomRunHooks(), # Run hooks pass in Runner instance
    context=test_data,  # Pass custom data to the context
)