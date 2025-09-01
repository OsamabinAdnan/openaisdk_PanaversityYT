## **Model Setting Cont.**

- `max-token:`
- `reasoning:`
- `metadata:` 
    - For tracing and debugging, go to [log](https://platform.openai.com/logs), enter your key and value of your metadata to search it.
- `store:` 
    - Whether to store or not agent run detail on log
- `include_usage:`
- `response_include:`
    
    ![response include example](media/response_include.png)

    - **code_interpreter_call.outputs**
    ![code_interpreter_call.outputs](media/code_interpreter_call.outputs.png)

    - **computer_call_output.output.image_url**
    ![computer_call_output.output.image_url](media/computer_call_output.output.image_url.png)

    - **file_search_call.results**
    ![file_search_call.results](media/file_search_call.results.png)

        * **Example**
        ![Example of file search](media/example_file_search_call.results.png)

    - **message.input_image.image_url**
    ![message.input_image.image_url](media/message.input_image.image_url.png)

    - **message.output_text.logprobs**
    ![message.output_text.logprobs](media/message.output_text.logprobs.png)

    - **reasoning.encrypted_content**
    ![reasoning.encrypted_content](media/reasoning.encrypted_content.png)

- `resolve (method):`
- `to_json_dict(method):`