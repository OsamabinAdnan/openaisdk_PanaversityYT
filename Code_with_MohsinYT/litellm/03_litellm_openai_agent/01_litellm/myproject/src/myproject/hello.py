from litellm import completion
import os

os.environ["GEMINI_API_KEY"] = "MY_GEMINI_API_KEY"

def gemini():
    response = completion(
        model="gemini/gemini-1.5-flash",
        messages=[{ "content": "Hello, how are you?","role": "user"}]
    )

    print(response)

def gemini2():
    response = completion(
        model="gemini/gemini-2.0-flash-exp",
        messages=[{ "content": "Hello, how are you?","role": "user"}]
    )

    print(response)

if __name__ == "__main__":
    gemini()
    gemini2()