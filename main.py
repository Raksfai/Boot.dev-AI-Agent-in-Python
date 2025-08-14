import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from system_prompt import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        print("Error 1")
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

    # GenerateContentResponse = client.models.generate_content(model="gemini-2.0-flash", contents=messages)

    GenerateContentResponse = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print(GenerateContentResponse.text)
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {GenerateContentResponse.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {GenerateContentResponse.usage_metadata.candidates_token_count}")
    else:
        print(GenerateContentResponse.text)

if __name__ == "__main__":
    main()

