import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from config import MODEL_NAME
from functions.call_functions import available_functions

from functions.call_functions import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError


client = genai.Client(api_key = api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

args = parser.parse_args()

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

response = client.models.generate_content(
    model = MODEL_NAME,
    contents=messages,
    config = types.GenerateContentConfig(
        tools = [available_functions],
        system_instruction=system_prompt
    )

)


if response.usage_metadata is None:
    raise RuntimeError

if args.verbose:
    print("User prompt: ", args.user_prompt)
    print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
    print("Response tokens: ", response.usage_metadata.candidates_token_count)




if response.function_calls:
    for function_call in response.function_calls:
        function_call_res = call_function(function_call=function_call)

        if function_call_res.parts is None:
            raise Exception
        
        elif function_call_res.parts[0].function_response is None:
            raise Exception
        
        elif function_call_res.parts[0].function_response.response is None:
            raise Exception
    

        if args.verbose:
            print(f"-> {function_call_res.parts[0].function_response.response}")

else:
    print(response.text)