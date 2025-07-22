# Python Expert Agent with Guardrails

In the context of OpenAI's Agent SDK, a guardrail refers to mechanisms or constraints put in place to ensure that an AI agent behaves safely, predictably, and within defined boundaries while executing tasks autonomously. These are crucial in agentic AI, where agents can plan, act, and use tools dynamically.

## Guardrail Concept in OpenAI Agent SDK
Guardrails define safety, ethical, and operational constraints that shape an agent's behavior—ensuring alignment with human intent, policy compliance, and robust error handling during tool use and autonomous decision-making.

They help:

* Restrict tool access or input/output formats
* Validate or filter agent actions
* Enforce business or safety policies
* Prevent unintended or harmful behaviors

## Project Implementation

This project demonstrates the practical implementation of guardrails using a Python Expert Agent. The implementation is split across two files:

1. `Input_Guardrail.py`: Implements input validation guardrails
2. `Input_Output_Guardrail.py`: Implements both input and output validation guardrails

### Key Features

- **Input Validation**: Ensures queries are Python-related
- **Output Validation**: Verifies responses maintain Python relevance (in Input_Output_Guardrail.py)
- **Interactive Chat Interface**: Built with Chainlit
- **Gemini API Integration**: Uses Google's Gemini model through OpenAI-compatible endpoint

## Technical Architecture

### Components

1. **Input Guardrails Agent**
   - Validates incoming queries
   - Uses Pydantic models for type validation
   - Filters non-Python content

2. **Output Guardrails Agent** (In Input_Output_Guardrail.py)
   - Validates agent responses
   - Ensures Python-appropriate content
   - Provides additional safety layer

3. **Main Agent**
   - Processes Python queries
   - Provides expert responses
   - Integrates with both guardrail systems

### Data Models

```python
# Input Validation
class OutputPythonType(BaseModel):
    is_python_related: bool
    reasoning: str

# Output Validation (In Input_Output_Guardrail.py)
class MessageOutput(BaseModel):
    response: str

class PythonOutput(BaseModel):
    is_python: bool
    reasoning: str
```

## Setup and Usage

1. **Environment Configuration**
   ```bash
   # Create .env file with
   GEMINI_API_KEY=your_api_key_here
   ```

2. **Run the Application**
   ```bash
   # For basic input guardrails
   chainlit run Input_Guardrail.py

   # For both input and output guardrails
   chainlit run Input_Output_Guardrail.py
   ```

3. **Interact with the Agent**
   - The agent welcomes users
   - Accepts Python-related queries
   - Provides helpful responses
   - Rejects non-Python content

## Error Handling

The system handles various error scenarios:
- Input validation errors (InputGuardrailTripwireTriggered)
- Output validation errors (OutputGuardrailTripwireTriggered)
- API key validation
- Invalid query handling

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Open a pull request

## License

This project is open-source and available under the MIT License.of OpenAI's Agent SDK, a guardrail refers to mechanisms or constraints put in place to ensure that an AI agent behaves safely, predictably, and within defined boundaries while executing tasks autonomously. These are crucial in agentic AI, where agents can plan, act, and use tools dynamically.

## **Guardrail Concept in OpenAI Agent SDK:**
---
Guardrails define safety, ethical, and operational constraints that shape an agent’s behavior—ensuring alignment with human intent, policy compliance, and robust error handling during tool use and autonomous decision-making.

They help:

* Restrict tool access or input/output formats

* Validate or filter agent actions

* Enforce business or safety policies

* Prevent unintended or harmful behaviors