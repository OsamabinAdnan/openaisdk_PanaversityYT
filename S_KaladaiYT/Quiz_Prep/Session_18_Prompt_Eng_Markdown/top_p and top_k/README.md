## **Prompt Engineering**

- **`top_k=5`** ==> Use only top (you value here which is `5`) words will be selected
    
    - Example: if top_k=5, the model will only consider the top 5 most probable options and ignore the rest.
    - Smaller top_k → more focused, predictable answers.
    - Larger top_k → more variety, but risk of randomness.

- **`top_p=0.9`** ==> Use only top (you value from `0.0 (0%)` to `1.0 (100%)`, here is `90%`) of vocabulary

    - Example: if p=0.9, the model will include tokens until they cover 90% of the probability mass.
    - it will pick tokens (every token has predetermine probability) until 90% token included respect to probability.

- `frequency_penalty=0.5` ==> Avoid repeating words

    - Penalizes a token based on how frequently it has appeared so far
    - Range: `-2.0 → +2.0`
    - Default: `0 (no penalty).`
    - `Higher value (e.g., 1.0 → 2.0):` Strongly discourages repetition, forces varied wording.
    - `Lower/negative value:` Encourages the model to repeat words more often.

- `presence_penalty=0.3` ==> Encourage new topics
    
    - Penalizes a token (word) if it has already appeared in the text.
    - Range: `-2.0 → +2.0`
    - Default: `0 (no penalty).`
    - `Higher value (e.g., 1.0 → 2.0):` The model avoids reusing the same words, pushes it toward introducing new concepts
    - `Lower/negative value (e.g., -1.0):` The model is more likely to repeat or stick to the same themes.