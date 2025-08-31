## **Model Setting**

- **temperature:** Check docs [Panaversity Repo](https://github.com/panaversity/learn-agentic-ai/tree/main/01_ai_agents_first/07_model_settings)

- **top_p:** [Article for better understanding](https://www.ibm.com/docs/en/watsonx/saas?topic=prompts-model-parameters-prompting)

- **frequency penalty:** (`frequency_penalty` is used to reduce the model’s tendency to repeat the same words or phrases. `Range: -2.0 to 2.0`,  `Default value: 0`)
    * A positive value (e.g., 1.0) discourages repetition (penalizes frequent tokens).
    * A negative value (e.g., -1.0) encourages repetition.
    * 0 means no effect (default behavior).

    For more details regarding parameters [Learn Prompting](https://learnprompting.org/blog/llm-parameters)

- **presence penalty:** (`presence_penalty` is used to reduce the model’s tendency to reuse tokens that have already appeared in the output, i.e., Encourage new topics, `Range: -2.0 to 2.0`)
    * `Positive values` penalize new tokens that have appeared in the generated text, encouraging novelty.
    * `Negative values` reward previously used tokens, encouraging repetition.

- **truncation:** In the OpenAI SDK, the `truncation` parameter in ModelSetting tells the model how to handle input text that exceeds the model’s context length (token limit).

    `"auto"` 
    - The SDK will automatically truncate the input from the beginning (oldest tokens) so the most recent text fits within the model’s maximum token limit.
    - This is usually the safest option.

    `"disabled"`
    - No truncation is applied. If your input is too long for the model’s context window, the request will fail with an error instead of being trimmed.

    `None (default)`
    - Equivalent to not setting anything; the model decides the handling (usually behaves like "auto" unless overridden).
