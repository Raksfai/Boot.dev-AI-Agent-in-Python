import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

content = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
GenerateContentResponse = client.models.generate_content(model="gemini-2.0-flash", contents=content)
print(GenerateContentResponse.text)
print(f"Prompt tokens: {GenerateContentResponse.usage_metadata.prompt_token_count}")
print(f"Response tokens: {GenerateContentResponse.usage_metadata.candidates_token_count}")

def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()

