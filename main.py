import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions


def main():
    load_dotenv()
    # Check that there is an API key and a GenAI client.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set in the environment variables.")
        exit(1)

    client = genai.Client(api_key=api_key)
    model_name = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    args = sys.argv[1:]
    # check if --verbose is written in the prompting argument. 
    verbose = "--verbose" in args
    if verbose:
        args.remove("--verbose")

    # Ensure user_prompt is always defined. Use default prompt when none provided.
    if not args:
        user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    else:
        user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model = model_name, 
        contents = messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )

    # Verify that usage_metadata is not None
    if response.usage_metadata is None:
        raise RuntimeError("Failed to retrieve usage metadata from the Gemini API response.")

    # if have --verbose written in the prompting argument, will print a lengthier explanation of the prompt, the text, and how many tokens it used.
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    # for any prompt, it will print out a response and text.
    if not response.function_calls:
        print("Response: ")        
        print(response.text)
        return
    
    print("\nFunctions: ")
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")


if __name__ == "__main__":
    main()