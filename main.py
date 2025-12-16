import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content
                           , schema_write_file, schema_run_python_file]
)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    if response.usage_metadata is None:
        raise RuntimeError("the usage metadata is empty")

    prompt_tokens_number = response.usage_metadata.prompt_token_count
    response_tokens_number = response.usage_metadata.candidates_token_count
    response_text = response.text

    if verbose:
        print(f"Prompt tokens: {prompt_tokens_number}")
        print(f"Response tokens: {response_tokens_number}")
    response_func_calls = response.function_calls
    function_call_parts = []
    if not response_func_calls:
        print(response_text)
        return
    if response_func_calls:
        for func in response_func_calls:
            function_call_result = call_function(func, verbose=verbose)
            if (
                not function_call_result.parts
                or function_call_result.parts[0].function_response is None
            ):
                raise RuntimeError("Function call result missing function_response")
            function_call_parts.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    function_name = function_call_part.name
    func = function_map.get(function_name)
    if func is None:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
    else:
        result = func(**args)
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    generate_content(client, messages, args.verbose)

if __name__ == "__main__":
    main()
