import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
print(f"DEBUG: api_key={api_key[:10]}..." if api_key else "DEBUG: api_key NOT FOUND")
if not api_key:
    # Try manual load if dotenv failed
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "GEMINI_API_KEY=" in line:
                    api_key = line.split("=")[1].strip()
                    print(f"DEBUG: Manual load api_key={api_key[:10]}...")
                    break

genai.configure(api_key=api_key)

print("--- Listing Models ---")
for m in genai.list_models():
    if 'embedContent' in m.supported_generation_methods:
        print(f"Model: {m.name}")

print("\n--- Testing Embedding ---")
content = "温かみのある木目調"
models_to_test = ["models/gemini-embedding-001", "models/text-embedding-004"]

for model_name in models_to_test:
    print(f"\nTesting model: {model_name}")
    
    # Test without task_type
    try:
        res = genai.embed_content(model=model_name, content=content)
        print(f"  Success without task_type. Dim: {len(res['embedding'])}")
    except Exception as e:
        print(f"  Failed without task_type: {e}")

    # Test with task_type retrieval_query
    try:
        res = genai.embed_content(model=model_name, content=content, task_type="retrieval_query")
        print(f"  Success with task_type='retrieval_query'. Dim: {len(res['embedding'])}")
    except Exception as e:
        print(f"  Failed with task_type='retrieval_query': {e}")
