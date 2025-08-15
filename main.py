import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from system_prompt import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    if len(sys.argv) > 1:
        user_prompt = sys.argv[1]
    else:
        print("Error 1")
        sys.exit(1)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )
    
    

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
        check_function_calls(GenerateContentResponse)
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {GenerateContentResponse.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {GenerateContentResponse.usage_metadata.candidates_token_count}")
    else:
        check_function_calls(GenerateContentResponse)

def check_function_calls(GenerateContentResponse):
    if GenerateContentResponse.function_calls is not None:
        for call in GenerateContentResponse.function_calls:
            print(f"Calling function: {call.name}({call.args})")   
    else:
        print(GenerateContentResponse.text)

if __name__ == "__main__":
    main()

