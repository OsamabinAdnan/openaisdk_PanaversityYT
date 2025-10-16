from dotenv import load_dotenv
import os
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, enable_verbose_stdout_logging
from openai import AsyncOpenAI
from rich import print

load_dotenv()

# enable_verbose_stdout_logging()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

BASE_URL = os.getenv("BASE_URL")
if not BASE_URL:
    raise ValueError("BASE_URL environment variable not set")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool(strict_mode=False)
def file_and_folder_handler(
    file_name:str | None = None,
    folder_name:str | None = None,
    content: str | None = None,
    file_path: str | None = None,
    read: bool | None = None,
):
    try:
        # All msg will append in empty list
        result_messages = []

        # Create folder logic
        if folder_name:
            os.makedirs(folder_name, exist_ok=True)
            result_messages.append(f"Folder '{folder_name}' created successfully.")
        
        # Read and FilePath logic

        if read and file_path:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_data = f.read()
                return f"Content of '{file_path}':\n{file_data}"
            else:
                return f"File '{file_path}' does not exist."
        
        # Create file logic
        if file_name:
            if folder_name:
                full_path = os.path.join(folder_name, file_name)
            else:
                full_path = file_name
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content if content else "")
            
            result_messages.append(f"File '{full_path}' created successfully.")
            if content:
                result_messages.append(f"Content of '{full_path}' updated successfully.")
        
        return "\n".join(result_messages)
        

    except Exception as e:
        print(f"An error occurred: {e}")


file_handler_agent = Agent(
    name="File Handler Agent",
    instructions="""
        You are helpful file manager and assistant, 
        1) Create folder and file and per user request.
        2) Write, or append and read file content as per user request.
        3) You should use the tool 'file_and_folder_handler' in order to create a file, folder operations.
        4) Generate any things, any type of file, folder and content as per user request.
        5) Use professional emojis when possible in your responses.

        * **Example of what you can do**
            - Create a folder name 'my_folder'
            - Inside that folder, create a file name e.g. my_file.html or my_file.js or my_file.py or my_file.txt etc.
    """,
    model=llm_model,
    tools=[file_and_folder_handler],
)

result = Runner.run_sync(
    file_handler_agent,
    # "Create file by the name Osama.txt in the folder of name Osama, and write 'My name is Osama bin Adnan' in the file.",
    
    # "Create html file by the name todo_list.html in the folder of name Osama, and write a html todo list of 3 items in the file. The first item should be 'Buy groceries', the second item should be 'Clean the house', and the third item should be 'Pay bills'. Also add css in that file for styling.",
    
    # "Hello!, how are you?",
    
    "Create a file named index.html inside a folder called Osama. Within this file, implement a responsive and animated To-Do List application using HTML, CSS, and JavaScript. Include all necessary CSS styling directly within the same index.html file (using internal styles) to ensure a visually appealing and user-friendly interface."
    
    
)

print(result.final_output)