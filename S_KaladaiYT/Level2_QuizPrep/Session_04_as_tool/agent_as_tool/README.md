## **Agent as_tool**

Transform this agent into a `tool`, callable by other agents.

* This is different from handoffs in two ways:
    1. In handoffs, the new agent receives the conversation history. In this tool, `the new agent receives generated input`.
    2. In handoffs, the new agent takes over the conversation. In this tool, `the new agent is called as a tool, and the conversation is continued by the original agent.`

* **Parameters**

    - **`tool_name:`** The name of the tool. If not provided, the agent's name will be used.
    - **`tool_description:`** The description of the tool, which should indicate what it does and when to use it.
    - **`custom_output_extractor:`** A function that extracts the output from the agent. If not provided, the last message from the agent will be used.
    - **`is_enabled:`** Whether the tool is enabled. Can be a bool or a callable that takes the run context and agent and returns whether the tool is enabled. Disabled tools are hidden from the LLM at runtime.