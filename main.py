import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


def main():
    load_dotenv()

    args = sys.argv[1:]
    argument_verbose = "--verbose"
    verbose = argument_verbose in args

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    if argument_verbose in args:
        list_arguments = []
        for arg in args: 
            if arg != argument_verbose:
                list_arguments.append(arg)
        user_prompt = " ".join(list_arguments)
    else:
        user_prompt = " ".join(args)



    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, user_prompt, verbose)


def generate_content(client, messages, user_prompt, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()