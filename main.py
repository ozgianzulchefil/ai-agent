import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_files_info import get_files_info
from functions.get_file_content import schema_get_file_content
from functions.get_file_content import get_file_content
from functions.run_python_file import schema_run_python_file
from functions.run_python_file import run_python_file
from functions.write_file import schema_write_file
from functions.write_file import write_file


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

    generate_content(client, messages, system_prompt, verbose, user_prompt)

FUNCTIONS = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

function_call_part = types.FunctionCall(
    name = "",
    args = {},
)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name

    kwargs = dict(function_call_part.args or {})
    if "file" in kwargs and "file_path" not in kwargs:
        kwargs["file_path"] = kwargs.pop("file")
    kwargs["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_name not in FUNCTIONS:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    func = FUNCTIONS[function_name]
    function_result = func(**kwargs)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
            )
        ],
    )


def generate_content(client, messages, system_prompt, verbose, user_prompt):

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
            ]
    )
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt,),
    )

    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    print("Response:")
    if response.function_calls:
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=verbose)
            if not function_call_result.parts or not function_call_result.parts[0].function_response:
                raise RuntimeError("Function call returned no function_response")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()