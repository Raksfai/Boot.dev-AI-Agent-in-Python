import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from system_prompt import system_prompt
from call_function import available_functions, call_function

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
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        check_function_calls(GenerateContentResponse, True)
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {GenerateContentResponse.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {GenerateContentResponse.usage_metadata.candidates_token_count}")
    else:
        check_function_calls(GenerateContentResponse)

def check_function_calls(GenerateContentResponse, verbose=False):
    if GenerateContentResponse.function_calls is not None:
        for call in GenerateContentResponse.function_calls:
            try:
                result = call_function(call, verbose)
                if (result.parts 
                    and len(result.parts) > 0 
                    and hasattr(result.parts[0], "function_response") 
                    and hasattr(result.parts[0].function_response, "response")
                    ):

                    if verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                    else:
                        raise Exception("Function call result did not contain expected function_response")
            except Exception as e:
                raise e
            
    else:
        print(GenerateContentResponse.text)

if __name__ == "__main__":
    main()

