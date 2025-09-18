## **Points to be noted from this lecture**

### **Trace**

- We have `trace function` and `Trace class` as well
- `Return type` of trace function is Trace class
- Create a new trace. The trace will not be started automatically; you should either use it as a context manager (`with trace(...):`) or call `trace.start()` + `trace.finish()` manually.


route to follow for below code ==> `agents -> tracing -> create.py`

```python
def trace(
    workflow_name: str,
    trace_id: str | None = None,
    group_id: str | None = None,
    metadata: dict[str, Any] | None = None,
    disabled: bool = False,
) -> Trace:
```

### **Span and its types**

```python
class SpanData(abc.ABC):
    """
    Represents span data in the trace.
    """

    @abc.abstractmethod
    def export(self) -> dict[str, Any]:
        """Export the span data as a dictionary."""
        pass

    @property
    @abc.abstractmethod
    def type(self) -> str:
        """Return the type of the span."""
        pass
```

- All Span data types inherit from SpanData class having 2 methods as mentioned above, so all types having these 2 method by default

    - **`AgentSpanData:`**
        *  Represents an Agent Span in the trace.
        *  Includes name, handoffs, tools, and output type.
        *  `return type is "agent"`
    
    - **`FunctionSpanData`**
        * Represents a Function Span in the trace.
        * Includes input, output and MCP data (if applicable).
        * `return type is "function"`
    
    - **`GenerationSpanData`**
        * Represents a Generation Span in the trace.
        * Includes input, output, model, model configuration, and usage.
        * `return type is "generation"`
    
    - **`ResponseSpanData`**
        * Represents a Response Span in the trace.
        * Includes response and input.
        * `return type is "response"`

    - **`HandoffSpanData`**
        * Represents a Handoff Span in the trace.
        * Includes source and destination agents.
        * `return type is "handoff"`

    - **`CustomSpanData`**
        * Represents a Custom Span in the trace.
        * Includes name and data property bag.
        * `return type is "custom"`

    - **`GuardrailSpanData`**
        * Represents a Guardrail Span in the trace.
        * Includes name and triggered status.
        * `return type is "guardrail"`

    - **`TranscriptionSpanData`**
        * Represents a Transcription Span in the trace.
        * Includes input, output, model, and model configuration.
        * `return type is "transcription"`

    - **`SpeechSpanData`**
        * Represents a Speech Span in the trace.
        * Includes input, output, model, model configuration, and first content timestamp.
        * `return type is "speech"`

    - **`SpeechGroupSpanData`**
        * Represents a Speech Group Span in the trace.
        * `return type is "speech_group"`

    - **`MCPListToolsSpanData`**
        * Represents an MCP List Tools Span in the trace.
        * Includes server and result.
        * `return type is "mcp_tools"`

### **Trace methods**

route to follow for trace method ==> `agents -> tracing -> traces.py`

1) `start`
2) `finish`
3) `export`

