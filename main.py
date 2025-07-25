import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    print("Hello from aia!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")  
    client = genai.Client(api_key=api_key)
    prompt = sys.argv[1]
    if len(prompt) < 2:
        print("No prompt provided.  Program Terminated.")
        sys.exit(1)
    messages = [types.Content(role="user", parts=[types.Part(text = prompt)])]
    response = client.models.generate_content(model = "gemini-2.0-flash-001", 
                                              contents = messages)
    
    user_prompt = sys.argv[1]
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        print(f"User prompt:  {user_prompt}")
        print(f"Prompt tokens:  {prompt_tokens}")
        print(f"Response tokens:  {response_tokens}")

    print(response.text)
    

if __name__ == "__main__":
    main()
