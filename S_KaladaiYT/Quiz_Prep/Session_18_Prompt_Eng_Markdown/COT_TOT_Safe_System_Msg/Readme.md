## **Chain of thoughs prompting, Tree of thoughts prompting and Safe system messages for sensitive data**

### **Chain of thoughts (CoT)**

- `Method:` Ask the model to show intermediate reasoning steps before giving the final answer.
- `Goal:` Improve reasoning on math, logic, and multi-step problems.
- `In OpenAI SDK:` Done by prompting (e.g., “Let’s think step by step”).

**Example:**
```python
prompt = "Q: If there are 3 apples and you take away 2, how many do you have? Let's think step by step."
```

```bash
Step 1: You start with 3 apples.
Step 2: You take away 2 apples.
Step 3: Therefore, you have 2 apples with you.
Answer: 2
```

![COT](media/COT%20prompting.png)

---

### **Tree of Thoughts Prompting (ToT)**

Extension of CoT.

Instead of a single reasoning path, the model explores multiple reasoning branches (like a decision tree).

- `Goal:` Evaluate different solution paths → choose the best.
- `In practice:` Requires orchestration (often external code/agents) to guide the model through branches.

**Example:**
```python
prompt = """
    Problem: Choose the best fruit to eat for energy: apple, banana, or orange.
    Think of different reasons for each option, then pick the best.
    """
```

```bash
Path 1: Apple – good fiber, moderate sugar.
Path 2: Banana – high sugar, potassium boost.
Path 3: Orange – vitamin C, hydration.

Best choice: Banana (quick energy and potassium)
```

![ToT](media/ToT%20prompting.png)
---
### **Safe System Messages (Sensitive Data)**

- In OpenAI SDK, system messages define model behavior.

- For sensitive data handling:

    * Use system messages to instruct the model not to reveal, store, or misuse private data.

**Example:**

```python
    system_message = {
    "role": "system",
    "content": "You are a safe assistant. Never reveal passwords, API keys, or personal information."
    }

    user_message = {
    "role": "user",
    "content": "Tell me my API key."
    }

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[system_message, user_message]
    )

    print(response.choices[0].message.content)
```

```bash
I’m sorry, I cannot reveal API keys or sensitive information.
```

![Safe System Messages](media/Safe%20System%20message%20(sensitive%20data).png)

In short:
- `CoT` = one reasoning path
- `ToT` = multiple reasoning paths and choose the best one
- `Safe system messages` = guardrails for sensitive data