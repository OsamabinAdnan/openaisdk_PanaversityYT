# Agent Hooks Demo Project

This project demonstrates the implementation and usage of hooks in an agent-based system using the OpenAI SDK. It showcases two different types of hooks: Agent Hooks and Runner Hooks, along with a simple number generation and multiplication workflow.

## Project Structure

- `agent_hook.py`: Implements the Agent-level hooks using `AgentHooks`
- `run_hook.py`: Implements the Runner-level hooks using `RunHooks`

## Features

- Integration with Gemini API (via OpenAI-compatible endpoint)
- Custom hook implementations for monitoring agent activities
- Multi-agent system with handoff capabilities
- Tool integration for random number generation and multiplication

## Prerequisites

- Python 3.x
- OpenAI SDK
- Environment variables:
  - `GEMINI_API_KEY`: Your Gemini API key

## Hooks Implementation

### Agent Hooks (`agent_hook.py`)

The `My_Agent_Hooks` class implements hooks at the agent level, tracking:
- Agent start/end events
- Tool execution start/end
- LLM interactions
- Agent handoffs

Key methods:
```python
- on_start()
- on_end()
- on_handoff()
- on_tool_start()
- on_tool_end()
- on_llm_start()
- on_llm_end()
```

### Runner Hooks (`run_hook.py`)

The `My_Runner_Hook` class implements hooks at the runner level, tracking:
- Agent execution
- Tool usage
- LLM interactions
- Handoffs between agents

Key methods:
```python
- on_agent_start()
- on_agent_end()
- on_tool_start()
- on_tool_end()
- on_handoff()
- on_llm_start()
- on_llm_end()
```

## Agents

The project includes three agents:

1. **Start Agent**: Generates a random number and decides whether to hand off to the Multiply Agent
2. **Multiply Agent**: Multiplies numbers by 2
3. **Weather Agent**: Provides weather information (demo purposes)

## Tools

Two function tools are implemented:
- `random_number(max: int)`: Generates a random number up to the specified maximum
- `multiply_by_two(x: int)`: Multiplies a number by 2

## Usage

1. Set up your environment variables:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

2. Run the application:
   ```bash
   python run_hook.py
   ```

3. Enter a maximum number when prompted. The system will:
   - Generate a random number
   - If odd, multiply it by 2
   - Display the result along with detailed hook events

## Event Tracking

Both implementations use an event counter to track the sequence of operations. Each hook method prints detailed information about:
- The current event number
- The type of event (start, end, handoff, etc.)
- The agent or tool involved
- Additional context specific to the event type

## Sample Output

When running the application, you'll see detailed event logs such as:
```bash
Enter a max number: 121
### Agent Started ### `1`, Agent: `Start Agent` started.
### LLM Started ### `2`: LLM started for agent: `Start Agent`.
### LLM Ended ### `3`: LLM ended for agent: `Start Agent`. Response: `ResponseFunctionToolCall(arguments='{"max":121}', call_id='',
name='random_number', type='function_call', id='__fake_id__', status=None)`.
### Tool Started ### `4`: Tool: `random_number` started. Agent: `Start Agent`
Random number: 45
### Tool Ended ### `5`: Tool: `random_number` ended with 45. Agent: `Start Agent`
### LLM Started ### `6`: LLM started for agent: `Start Agent`.
### LLM Ended ### `7`: LLM ended for agent: `Start Agent`. Response: `ResponseFunctionToolCall(arguments='{}', call_id='',
name='transfer_to_multiply_agent', type='function_call', id='__fake_id__', status=None)`.
### Handoff ### `8`: Handoff from `Start Agent` to `Multiply Agent`.
### Agent Started ### `9`, Agent: `Multiply Agent` started.
### LLM Started ### `10`: LLM started for agent: `Multiply Agent`.
### LLM Ended ### `11`: LLM ended for agent: `Multiply Agent`. Response: `ResponseFunctionToolCall(arguments='{"x":45}', call_id='',
name='multiply_by_two', type='function_call', id='__fake_id__', status=None)`.
### Tool Started ### `12`: Tool: `multiply_by_two` started. Agent: `Multiply Agent`
### Tool Ended ### `13`: Tool: `multiply_by_two` ended with 90. Agent: `Multiply Agent`
### LLM Started ### `14`: LLM started for agent: `Multiply Agent`.
### LLM Ended ### `15`: LLM ended for agent: `Multiply Agent`. Response: `ResponseOutputMessage(id='__fake_id__',
content=[ResponseOutputText(annotations=[], text='The random number is 45. If I multiply it by 2, I get 90. \n', type='output_text',
logprobs=None)], role='assistant', status='completed', type='message')`.
### Agent Ended ### `16`: Agent: `Multiply Agent` ended.
Result: The random number is 45. If I multiply it by 2, I get 90.

Done!
```

## Note

This is a demonstration project showing how to implement and use hooks for monitoring and tracking agent behavior in a multi-agent system. The hooks provide valuable insights into the execution flow and can be extended for debugging, logging, or monitoring purposes.
