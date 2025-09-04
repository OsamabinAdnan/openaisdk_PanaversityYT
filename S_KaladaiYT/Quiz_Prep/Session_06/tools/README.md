***We have discussed below topics in this session***

* **function_tool (decorator)**
    - **`failure_error_function:`**

* **Model Setting**
    - **`tool choice:`** 
        * Either you can select `auto`, `required` or `none`and you can also write `tool name` here to called specific tool
        * The different between **model setting** attribute of `tool_choice` and function_tool decorator of is_enable is:
            * In tool_choice option, tools have been passed to agent loop but LLM doesnt use them
                ![tool_choice example](media/tool_choice.png)
            ---
            * But in is_enabled option, tools have not been passed to agent loop.
                ![is_enabled example](media/is_enable.png)
    
    - **`parallel tool calls`**
        * Only run if we have OpenAI API
        * Suppose, if `parallal_tool_calls` is set as False and we have 2 tools to run then total turns will be 3:
            - first tool run
            - second tool run
            - LLM run and generated answer

* **Agent**
    - **`tool_use_behavior:`**
        * **`"run_llm_again":`** The default behavior. Tools are run, and then the LLM receives the results
            and gets to respond.
        * **`"stop_on_first_tool":`** The output from the first tool call is treated as the final result.
            In other words, it isn’t sent back to the LLM for further processing but is used directly
            as the final output.
        * **`StopAtTools (class):`** A list of tool names, any of which will stop the agent from running further.
            The final output will be the output of the first matching tool call. The LLM does not process the result of the tool call
        * **`TooltoFinalOutputFunction (callable):`**

            ```python
                ToolsToFinalOutputFunction: TypeAlias = Callable[
                    [RunContextWrapper[TContext], list[FunctionToolResult]],
                    MaybeAwaitable[ToolsToFinalOutputResult],
                ]
            ```

            * **`ToolsToFinalOutputResult:`**
                - `is_final_output: bool` ==> Whether this is the final output. If False, the LLM will run again and receive the tool call output.
                - `final_output: Any | None = None` ==> The final output. Can be None if `is_final_output` is False,otherwise must match the `output_type` of the agent.
            
            * **`FunctionToolResult:`**
                - `tool: FunctionTool` ==> The tool that was run.
                - `output: Any` ==> The output of the tool.
                - `run_item: RunItem` ==>The run item that was produced as a result of the tool call.
    
    * **`reset_tool_choice: bool = True`**
    Whether to reset the tool choice to the default value after a tool has been called. Defaults
    to True. This ensures that the agent doesn't enter an infinite loop of tool usage.

    * **`(Agent) as_tool (method):`**
        ```python
        def as_tool(
            self,
            tool_name: str | None,
            tool_description: str | None,
            custom_output_extractor: Callable[[RunResult], Awaitable[str]] | None = None,
            is_enabled: bool
            | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]] = True,
        ) -> Tool:
        ```
        - Transform this agent into a tool, callable by other agents.

            This is different from handoffs in two ways:
            1) In handoffs, the new agent receives the conversation history. In this tool, the new agent
            receives generated input.
            2) In handoffs, the new agent takes over the conversation. In this tool, the new agent is
            called as a tool, and the conversation is continued by the original agent.
            Args:
                * `tool_name:` The name of the tool. If not provided, the agent's name will be used.
                * `tool_description:` The description of the tool, which should indicate what it does and
                    when to use it.
                * `custom_output_extractor:` A function that extracts the output from the agent. If not
                    provided, the last message from the agent will be used.
                * `is_enabled:` Whether the tool is enabled. Can be a bool or a callable that takes the run
                    context and agent and returns whether the tool is enabled. Disabled tools are hidden
                    from the LLM at runtime.

        - In OpenAI SDK, a `workflow` is the execution `trace` of how an agent handles a user query.
            * ***The main agent receives the input, decides whether to answer directly or call a tool.***
            * ***If a tool is called, it may itself be another specialized agent that processes the query and returns the result.***
            * ***Finally, the main agent collects that result and delivers the response back to the user.***