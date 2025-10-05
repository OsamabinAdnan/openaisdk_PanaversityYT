### **Projects**

- **`01:`**
    * tool use behavior
    * max turns

- **`02:`**
    * Raise Value Error in tool

- **`03:`**
    * Handoff (when you have 1 tool and 1 handoff agent)

- **`04:`**
    * Handoff (when you have 2 handoff agents), one will be ignored when your input required output from both.

- **`05:`**
    * tool choice required in Model Setting

- **`06:`**
    * tool choice required in Model Setting but max turn is 1

- **`07:`**
    * handoff function and its parameters

- **`08:`**
    * input filter parameter of handoff function
    * There are 3 parameters of `HandoffInputData`:
        - **input_history:** The input history before `Runner.run()` was called.
        - **pre_handoff_items:**  The items generated before the agent turn where the handoff was invoked.
        - **new_items:** The new items generated during the current agent turn, including the item that triggered the handoff and the tool output message representing the response from the handoff output.
    
    ***Condition 01: When input_history has given only***
    ```bash
        Creating trace Agent workflow with id trace_da874d9f55054f8299d4618b5f0f3842
        Setting current trace: trace_da874d9f55054f8299d4618b5f0f3842
        Creating span <agents.tracing.span_data.AgentSpanData object at 0x000001D51762ACB0> with id None
        Running agent Assistant (turn 1)
        Creating span <agents.tracing.span_data.GenerationSpanData object at 0x000001D51927CD10> with id None
        [
          {
            "content": "You are helpful assistant.",
            "role": "system"
          },
          {
            "role": "user",
            "content": "what is current weather in karachi?"
          }
        ]
        Tools:
        [
          {
            "type": "function",
            "function": {
              "name": "transfer_to_get_weather",
              "description": "Handoff to the get_weather agent to handle the request. get the weather for given city",
              "parameters": {
                "additionalProperties": false,
                "type": "object",
                "properties": {},
                "required": []
              }
            }
          }
        ]
        Stream: False
        Tool choice: NOT_GIVEN
        Response format: NOT_GIVEN

        LLM resp:
        {
          "content": null,
          "refusal": null,
          "role": "assistant",
          "annotations": null,
          "audio": null,
          "function_call": null,
          "tool_calls": [
            {
              "id": "function-call-9226487839774071482",
              "function": {
                "arguments": "{}",
                "name": "transfer_to_get_weather"
              },
              "type": "function"
            }
          ]
        }

        Creating span <agents.tracing.span_data.HandoffSpanData object at 0x000001D519723FD0> with id None
        #### Handoff invoked ####
        Filtering inputs for handoff
        Creating span <agents.tracing.span_data.AgentSpanData object at 0x000001D51774A940> with id None
        Running agent get_weather (turn 2)
        Creating span <agents.tracing.span_data.GenerationSpanData object at 0x000001D513CC63F0> with id None
        [
          {
            "content": "You must always respond: 'Today the weather is cloudy.",
            "role": "system"
          },
          {
            "role": "user",
            "content": "what is current weather in karachi?"
          }
        ]
        Tools:
        []
        Stream: False
        Tool choice: NOT_GIVEN
        Response format: NOT_GIVEN

        LLM resp:
        {
          "content": "Today the weather is cloudy.",
          "refusal": null,
          "role": "assistant",
          "annotations": null,
          "audio": null,
          "function_call": null,
          "tool_calls": null
        }

        Resetting current trace
        Today the weather is cloudy.
        Shutting down trace provider
        Shutting down trace processor <agents.tracing.processors.BatchTraceProcessor object at 0x000001D517632A50>
        Exported 6 items
    ```

    ***Condition 02: When both input_history and pre_handoff_items are given***
    ```bash
        Creating trace Agent workflow with id trace_d76c9d039d724a9199391cf51689cc8f
        Setting current trace: trace_d76c9d039d724a9199391cf51689cc8f
        Creating span <agents.tracing.span_data.AgentSpanData object at 0x00000272171BB200> with id None
        Running agent Assistant (turn 1)
        Creating span <agents.tracing.span_data.GenerationSpanData object at 0x00000272137E63F0> with id None
        [
          {
            "content": "You are helpful assistant.",
            "role": "system"
          },
          {
            "role": "user",
            "content": "what is current weather in karachi?"
          }
        ]
        Tools:
        [
          {
            "type": "function",
            "function": {
              "name": "transfer_to_get_weather",
              "description": "Handoff to the get_weather agent to handle the request. get the weather for given city",
              "parameters": {
                "additionalProperties": false,
                "type": "object",
                "properties": {},
                "required": []
              }
            }
          }
        ]
        Stream: False
        Tool choice: NOT_GIVEN
        Response format: NOT_GIVEN

        LLM resp:
        {
          "content": null,
          "refusal": null,
          "role": "assistant",
          "annotations": null,
          "audio": null,
          "function_call": null,
          "tool_calls": [
            {
              "id": "function-call-12640472227624817048",
              "function": {
                "arguments": "{}",
                "name": "transfer_to_get_weather"
              },
              "type": "function"
            }
          ]
        }

        Creating span <agents.tracing.span_data.HandoffSpanData object at 0x00000272192B4510> with id None
        #### Handoff invoked ####
        Filtering inputs for handoff
        Creating span <agents.tracing.span_data.AgentSpanData object at 0x000002721713C230> with id None
        Running agent get_weather (turn 2)
        Creating span <agents.tracing.span_data.GenerationSpanData object at 0x000002721929B230> with id None
        [
          {
            "content": "You must always respond: 'Today the weather is cloudy.",
            "role": "system"
          },
          {
            "role": "user",
            "content": "what is current weather in karachi?"
          }
        ]
        Tools:
        []
        Stream: False
        Tool choice: NOT_GIVEN
        Response format: NOT_GIVEN

        LLM resp:
        {
          "content": "Today the weather is cloudy.",
          "refusal": null,
          "role": "assistant",
          "annotations": null,
          "audio": null,
          "function_call": null,
          "tool_calls": null
        }

        Resetting current trace
        Today the weather is cloudy.
        Shutting down trace provider
        Shutting down trace processor <agents.tracing.processors.BatchTraceProcessor object at 0x00000272171C2A50>
        Exported 6 items
    ```
    ***Condition 03: When both input_history and new_items are given***
    ```bash
        Creating trace Agent workflow with id trace_c5d1290fa61144bb9d99943af425e06d
        Setting current trace: trace_c5d1290fa61144bb9d99943af425e06d
        Creating span <agents.tracing.span_data.AgentSpanData object at 0x000002091842EC10> with id None
        Running agent Assistant (turn 1)
        Creating span <agents.tracing.span_data.GenerationSpanData object at 0x0000020919E2CD10> with id None
        [
          {
            "content": "You are helpful assistant.",
            "role": "system"
          },
          {
            "role": "user",
            "content": "what is current weather in karachi?"
          }
        ]
        Tools:
        [
          {
            "type": "function",
            "function": {
              "name": "transfer_to_get_weather",
              "description": "Handoff to the get_weather agent to handle the request. get the weather for given city",
              "parameters": {
                "additionalProperties": false,
                "type": "object",
                "properties": {},
                "required": []
              }
            }
          }
        ]
        Stream: False
        Tool choice: NOT_GIVEN
        Response format: NOT_GIVEN

        LLM resp:
        {
          "content": null,
          "refusal": null,
          "role": "assistant",
          "annotations": null,
          "audio": null,
          "function_call": null,
          "tool_calls": [
            {
              "id": "function-call-3177714367773533619",
              "function": {
                "arguments": "{}",
                "name": "transfer_to_get_weather"
              },
              "type": "function"
            }
          ]
        }

        Creating span <agents.tracing.span_data.HandoffSpanData object at 0x000002091A2E00D0> with id None
        #### Handoff invoked ####
        Filtering inputs for handoff
        Creating span <agents.tracing.span_data.AgentSpanData object at 0x00000209182E9AE0> with id None
        Running agent get_weather (turn 2)
        Creating span <agents.tracing.span_data.GenerationSpanData object at 0x00000209148C63F0> with id None
        [
          {
            "content": "You must always respond: 'Today the weather is cloudy.",
            "role": "system"
          },
          {
            "role": "user",
            "content": "what is current weather in karachi?"
          },
          {
            "role": "assistant",
            "tool_calls": [
              {
                "id": "function-call-3177714367773533619",
                "type": "function",
                "function": {
                  "name": "transfer_to_get_weather",
                  "arguments": "{}"
                }
              }
            ]
          },
          {
            "role": "tool",
            "tool_call_id": "function-call-3177714367773533619",
            "content": "{\"assistant\": \"get_weather\"}"
          }
        ]
        Tools:
        []
        Stream: False
        Tool choice: NOT_GIVEN
        Response format: NOT_GIVEN

        LLM resp:
        {
          "content": "Today the weather is cloudy.",
          "refusal": null,
          "role": "assistant",
          "annotations": null,
          "audio": null,
          "function_call": null,
          "tool_calls": null
        }

        Resetting current trace
        Today the weather is cloudy.
        Shutting down trace provider
        Shutting down trace processor <agents.tracing.processors.BatchTraceProcessor object at 0x00000209181D2A50>
        Exported 6 items
    ```

    * You have to pass `input_history` in filter then you can play with `pre_handoff_items` and `new_items`

- **`09:`**
   