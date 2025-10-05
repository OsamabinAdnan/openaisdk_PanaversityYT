## **Model Settings**

- `temperature:` Range from 0.0 to 2.0
- `top_p:` Range from 0.0 to 1.0
- `tool_choice:` Range from ["auto", "required", "none"], by default it is auto
- `parallal tool choice:` True or False, by default it True
- `truncation:` Defaults to disabled
    * The truncation strategy to use for the model response.
        - `auto:` If the input to this Response exceeds the model's context window size, the model will truncate the response to fit the context window by dropping items from the beginning of the conversation.
        - `disabled (default):` If the input size will exceed the context window size for a model, the request will fail with a 400 error.
- `max_token:` Atleast you have to give 16 tokens, you can't give token less than 16 otherwise you will get Bad request error.
- `Model Settings Methods:`
    * `resolve:`Produce a new ModelSettings by overlaying any non-None values from the override on top of this instance.
    * `to_json_dict:` Return all parameters of model setting in JSON format.