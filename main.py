import os
from google import genai
from dotenv import load_dotenv
import argparse
def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User Prompt")
    args = parser.parse_args()
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if api_key == None:
        raise RuntimeError("No api key found, or it is None")
    prompt = args.prompt
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt
    )
    if response.usage_metadata == None:
        raise RuntimeError("the usage metadata is empty")
    
    prompt_tokens_number = response.usage_metadata.prompt_token_count
    response_tokens_number = response.usage_metadata.candidates_token_count
    response_text = response.text
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {prompt_tokens_number}")
    print(f"Response tokens: {response_tokens_number}")
    print(f"Response: \n{response_text}")

if __name__ == "__main__":
    main()
