## **Exception**

### **RunErrorDetails dataclass**

- Data collected from an agent run when an exception occurs.

### **AgentsException (Base class of all exception in OpenAI SDK)**

Bases: `Exception`

- Base class for all exceptions in the Agents SDK.

### **MaxTurnsExceeded**

Bases: `AgentsException`

- Exception raised when the maximum number of turns is exceeded.

### **ModelBehaviorError**

Bases: `AgentsException`

- Exception raised when the model does something unexpected, e.g. calling a tool that doesn't exist, or providing malformed JSON.

### **UserError**

Bases: `AgentsException`

- Exception raised when the user makes an error using the SDK.

### **InputGuardrailTripwireTriggered**

Bases: `AgentsException`

- Exception raised when a guardrail tripwire is triggered.

    #### **guardrail_result `instance-attribute`**

    - The result data of the guardrail that was triggered.

### **OutputGuardrailTripwireTriggered**

Bases: `AgentsException`

- Exception raised when a guardrail tripwire is triggered.

    #### **guardrail_result `instance-attribute`**

    - The result data of the guardrail that was triggered.

