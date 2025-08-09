import sys
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if len(sys.argv) > 1:
    content = sys.argv[1]
else:
    print("Error 1")
    sys.exit(1)
GenerateContentResponse = client.models.generate_content(model="gemini-2.0-flash", contents=content)
print(GenerateContentResponse.text)
print(f"Prompt tokens: {GenerateContentResponse.usage_metadata.prompt_token_count}")
print(f"Response tokens: {GenerateContentResponse.usage_metadata.candidates_token_count}")

def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()

