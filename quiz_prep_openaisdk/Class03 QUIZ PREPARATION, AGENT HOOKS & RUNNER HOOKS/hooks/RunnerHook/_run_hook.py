from agents import Runner, RunHooks, RunContextWrapper, TContext, Tool, AgentBase
from typing import Any, TypeVar


TAgent = TypeVar("TAgent", bound=AgentBase, default=AgentBase)
class MyCustomRunHook(RunHooks):
    """A class that receives callbacks on various lifecycle events in an agent run. Subclass and
    override the methods you need.
    """

    # class MyTestData(BaseModel):
    #     """An example Pydantic model for custom data."""
    #     name: str
    #     age: int

    # You can define your own custom data model here if needed and pass it to the context like RunContextWrapper[MyTestData].

    # on_agent_start: Called before the agent is invoked. Called each time the current agent changes.
    async def on_agent_start(self, context: RunContextWrapper[TContext], agent: TAgent) -> None:
        """Called before the agent is invoked. Called each time the current agent changes."""
        pass
    
    # on_agent_end: Called when the agent produces a final output.
    async def on_agent_end(
        self,
        context: RunContextWrapper[TContext],
        agent: TAgent,
        output: Any,
    ) -> None:
        """Called when the agent produces a final output."""
        pass
    
    # on_handoff: Called when a handoff occurs.
    async def on_handoff(
        self,
        context: RunContextWrapper[TContext],
        from_agent: TAgent,
        to_agent: TAgent,
    ) -> None:
        """Called when a handoff occurs."""
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

####################################### Class example for [TContext] #######################################

from dataclasses import dataclass, field

# T is a type variable, enabling the class to be generic—it can accept different types (int, str, etc.).
T=TypeVar("T")
@dataclass
# This declares a generic data class MyTest[T] where all three fields (id, idsub, abc) will be of the same type T.
class MyTest[T]():
    id:T
    idsub:T
    abc:T

output = MyTest[str](id="qwe", idsub="asd", abc="123")

######################### Pydantic example for validation #########################
# Pydantic is a data validation and settings management library for Python.
# It allows you to define data models with type annotations and perform validation automatically.
# Here, we define a Pydantic model MyTest that has three fields: id, idsub, and abc, all of which are integers.
# This is useful for ensuring that the data conforms to the expected types and structure,
# which can help prevent errors in your application.
from pydantic import BaseModel

class myTest(BaseModel):
    id: int
    idsub: int
    abc: int

@dataclass
class MyTest2[T]():
    mydata : T

output2 = MyTest2(myTest(id=1, idsub=2, abc=3))