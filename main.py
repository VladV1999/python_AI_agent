import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import argparse
from prompts import system_prompt

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    if response.usage_metadata is None:
        raise RuntimeError("the usage metadata is empty")

    prompt_tokens_number = response.usage_metadata.prompt_token_count
    response_tokens_number = response.usage_metadata.candidates_token_count
    response_text = response.text

    if verbose:
        print(f"Prompt tokens: {prompt_tokens_number}")
        print(f"Response tokens: {response_tokens_number}")
    print(f"Response: \n{response_text}")

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
