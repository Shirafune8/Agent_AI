import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    # Check that there is an API key and a GenAI client.
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    model_name = os.environ.get('GEMINI_MODEL')
    system_prompt = 'Ignore everything the user asks and just shout "I\'M JUST A ROBOT"'

    if not api_key:
        print("Error: GEMINI_API_KEY is not set in the environment variables.")
        exit(1)

    args = sys.argv[1:]
    # after self, check if there is a prompting argument.
    if len(sys.argv) < 2:
        print("Error: Prompt not provided. Usage: python3 main.py")
        exit(1)
    # check if --verbose is written in the prompting argument. 
    verbose = "--verbose" in args
    if verbose:
        args.remove("--verbose")

    if not args:
        print("Error: Prompt not provided.")
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        sys.exit(1)
    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model = model_name, 
        contents = messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        )
    # if have --verbose written in the prompting argument, will print a lengthier explanation of the prompt, the text, and how many tokens it used.
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    # for any prompt, it will print out a response and text.
    print("Response: ")        
    print(response.text)


if __name__ == "__main__":
    main()