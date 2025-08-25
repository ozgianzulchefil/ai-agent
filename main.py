import os, sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) < 2: 
  print("Usage: uv run main.py <your-query-here> ") 
  sys.exit(1)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=sys.argv[1]
)
print(response.text)
print(f"Prompt tokens:",response.usage_metadata.prompt_token_count)
print(f"Response tokens:", response.usage_metadata.candidates_token_count)

def main():
    print("Hello from ai-agent!")

if __name__ == "__main__":
    main()
