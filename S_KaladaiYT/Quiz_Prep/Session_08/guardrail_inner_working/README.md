# **Input/Output Guardrail: Decorator vs Class**

The decorators (@input_guardrail, @output_guardrail) are just shortcuts that wrap a function into the corresponding class.

You can manually create guardrails using the classes instead — they work the same.


### **✅ Example with decorator:**

```python
@input_guardrail
def block_if_empty(context, agent, user_input):
    if not user_input:
        return GuardrailFunctionOutput(
            output_info="Input was empty",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(output_info="OK", tripwire_triggered=False)
```

Here `block_if_empty` automatically becomes an `InputGuardrail`.

### **✅ Same thing without decorator:**

```python
def block_if_empty(context, agent, user_input):
    if not user_input:
        return GuardrailFunctionOutput("Input was empty", True)
    return GuardrailFunctionOutput("OK", False)

guardrail = InputGuardrail(guardrail_function=block_if_empty, name="block_if_empty")
```

Now `guardrail` is an `InputGuardrail` instance created directly with the class, instead of using the decorator.

### **🔑 Difference in short:**

* **Using decorators:**
    
    Cleaner syntax, automatically wraps your function into the right class.

* **Using classes directly:**

    You have more manual control (e.g., passing a custom `name` or dynamically constructing guardrails in code).

👉 In both cases, when you later call `.run()`, they return the same thing (`InputGuardrailResult` or `OutputGuardrailResult`).


## **1. Input Decorator (`@input_guardrail`)**

* **What it wraps?**
    - Wraps a sync/async function into an `InputGuardrail` class.

* **Function signature:**
    - The wrapped function must accept:

    ```python
    (context: RunContextWrapper[TContext], agent: Agent[Any], input: str | list[TResponseInputItem])
    ```

    and return either:

    - `GuardrailFunctionOutput` (sync), or
    - `Awaitable[GuardrailFunctionOutput]` (async).

* **What it returns?**

    - Returns an InputGuardrail[TContext] instance.
    - That object can later be executed via `.run()`which produces an `InputGuardrailResult`.

## **2. Output Decorator (`@output_guardrail`)**

* **What it wraps?**

    - Wraps a sync/async function into an `OutputGuardrail` class.

* **Function signature:**

    - The wrapped function must accept:

    ```python
    (context: RunContextWrapper[TContext], agent: Agent[Any], agent_output: Any)
    ```

    and return either:

    - `GuardrailFunctionOutput` (sync), or
    - `Awaitable[GuardrailFunctionOutput]` (async).

* **What it returns?**

    - Returns an `OutputGuardrail[TContext]` instance.
    - That object can later be executed via `.run()` which produces an `OutputGuardrailResult`.


## **3. GuardrailFunctionOutput**

- The `GuardrailFunctionOutput` is the standardized return type of any guardrail function (whether input or output).

    Here’s what it is:

    ```python
    @dataclass
    class GuardrailFunctionOutput:
        output_info: Any
        tripwire_triggered: bool

    ```
### **Meaning:**
* `output_info: Any`
    Optional metadata about what the guardrail checked.

    Example: `"Input contained profanity"` or a dictionary with validation details.

* `tripwire_triggered: bool`
    
    * This is the key flag 🚨.

        - True → the guardrail says "stop execution" (e.g., input/output failed validation).
        - False → safe to continue.

### **🔑 How it fits in the chain:**

* A decorated guardrail function must return a `GuardrailFunctionOutput`.
* The decorator (`@input_guardrail` / `@output_guardrail`) wraps that function into an `InputGuardrail` or `OutputGuardrail`.
* When `.run()` is called, the wrapper executes the function and packs the result into either:

    - `InputGuardrailResult` (for input guardrails)
    - `OutputGuardrailResult` (for output guardrails),
    
    which always contain a `GuardrailFunctionOutput` inside them.
