# **Tools**

## **Making tool using `FunctionTool` class directly**

* When you are making tool using **FunctionTool** class without function tool decorator `(@function_tool)`, we have to pass following parameters in it, they are mandatory:

    - name
    - description
    - params_json_schema
    - on_invoke_tool`

* See below code

```python
my_tool = FunctionTool(
    name="get_weather",
    description="Get the current weather for a given location.",
    params_json_schema=My_SCHEMA,
    on_invoke_tool=weather,
    strict_json_schema=False # set to False if you dont want city property to be required | default is True
)
```
* Remaining parameters are optional.

* You can set your own schema as well using.
    - You can get `Param json schema` from `.venv\Lib\site-packages\agents\strict_schema.py` where default schema is mentioned

    ```python
    # Default Schema
    _EMPTY_SCHEMA = {
    "additionalProperties": False,
    "type": "object",
    "properties": {},
    "required": [],
    }
    ```

    ```python
    # Modified schema
    My_SCHEMA = {
        "additionalProperties": False,
        "type": "object",
        "properties": {
            "city": {
                "type":"string"
            }
        },
        "required": [], # city property will show as required in required list when you see logs | if you dont want it to be required, set strict_json_schema function to False in `FunctionTool class`
    }
    ```

* The callable function we make for `on_invoke_tool` should be:
    - Awaitable (Async)
    - First Parameter should be context (as or not as, respect to requirement) a type of `RunContextWrapper` class

## ****@function_tool** decorator**

- Instead of using FunctionTool class, you can also use @function_tool decorator to make tool
- For function tool decorator,
    * You dont need to write schema separately, it will be generated automatically from function signature
    * You dont need to invoke tool separately, it will be invoked automatically
    * We used FunctionTool class when we want to have more control over schema and invocation

- **`name_override:`** If provided, use this name for the tool instead of the function's name.

- **`description_override:`** If provided, use this description for the tool instead of the function's docstring.

- **`docstring_style:`** If provided, use this style for the tool's docstring. If not provided, we will attempt to auto-detect the style.

- **`use_docstring_info:`** If True, use the function's docstring to populate the tool's description and argument descriptions. By default, it True, set to False if you dont want to send docstring info to tool schema

- **`failure_error_function:`** If provided, use this function to generate an error message when the tool call fails. The error message is sent to the LLM. If you pass None, then no error message will be sent and instead an Exception will be raised.

- **`strict_mode:`** Whether to enable strict mode for the tool's JSON schema. We *strongly* recommend setting this to True, as it increases the likelihood of correct JSON input. If False, it allows non-strict JSON schemas. For example, if a parameter has a default value, it will be optional, additional properties are allowed, etc. See here for more: https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses#supported-schemas. By default is True, set to False if you dont want to use required property (schema) for default values, like city in this case is set to default to "Karachi" so it is not required in required field of schema.

- **`is_enabled:`** Whether the tool is enabled. Can be a bool or a callable that takes the run context and agent and returns whether the tool is enabled. Disabled tools are hidden from the LLM at runtime. By default is True, set to False if you want to disable tool, it will not be give to LLMs.