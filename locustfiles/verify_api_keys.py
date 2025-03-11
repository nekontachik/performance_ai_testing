import json
import sys
import subprocess
import os
import argparse
from dotenv import load_dotenv

# Add the parent directory to sys.path to allow importing from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)

def verify_openai_key(api_key):
    print("Testing OpenAI API key...")
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("❌ OpenAI API key is not set")
        return False
    
    curl_cmd = [
        'curl', '-s',
        'https://api.openai.com/v1/chat/completions',
        '-H', f'Authorization: Bearer {api_key}',
        '-H', 'Content-Type: application/json',
        '-d', '{"model":"gpt-3.5-turbo","messages":[{"role":"system","content":"You are a helpful assistant."},{"role":"user","content":"Hello"}],"max_tokens":5}'
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and '"choices"' in result.stdout:
            print("✅ OpenAI API key is valid!")
            return True
        else:
            print(f"❌ OpenAI API key error")
            print(f"Error details: {result.stdout[:200]}")
            return False
    except Exception as e:
        print(f"❌ OpenAI API request failed: {str(e)}")
        return False

def verify_huggingface_key(api_key):
    print("Testing Hugging Face API key...")
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("❌ Hugging Face API key is not set")
        return False
    
    curl_cmd = [
        'curl', '-s',
        'https://api-inference.huggingface.co/pipeline/text-generation/gpt2',
        '-H', f'Authorization: Bearer {api_key}',
        '-H', 'Content-Type: application/json',
        '-d', '{"inputs":"Hello"}'
    ]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip() and not result.stdout.startswith('{"error'):
            print("✅ Hugging Face API key is valid!")
            return True
        else:
            print(f"❌ Hugging Face API key error")
            print(f"Error details: {result.stdout[:200]}")
            return False
    except Exception as e:
        print(f"❌ Hugging Face API request failed: {str(e)}")
        return False

def extract_key_from_file(file_path, key_name="api_key"):
    """Extract API key from a Python file."""
    try:
        with open(file_path, "r") as f:
            for line in f:
                if f"{key_name} =" in line and not line.strip().startswith("#"):
                    # Extract the value after the equals sign
                    value = line.split("=")[1].strip()
                    # Remove quotes and trailing comments
                    value = value.strip('"\'')
                    if "#" in value:
                        value = value.split("#")[0].strip()
                    return value
    except Exception as e:
        print(f"Warning: Could not extract key from {file_path}: {str(e)}")
    return None

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Verify API keys for AI services")
    parser.add_argument("--use-env", action="store_true", help="Use environment variables for API keys")
    parser.add_argument("--openai-key", help="OpenAI API key to verify")
    parser.add_argument("--hf-key", help="Hugging Face API key to verify")
    args = parser.parse_args()
    
    # Get API keys
    openai_key = None
    hf_key = None
    
    # Priority: 1. Command line args, 2. Environment variables, 3. Files
    if args.openai_key:
        openai_key = args.openai_key
    else:
        # Always use environment variables from .env file
        openai_key = os.getenv("OPENAI_API_KEY")
    
    if args.hf_key:
        hf_key = args.hf_key
    else:
        # Always use environment variables from .env file
        hf_key = os.getenv("HF_API_KEY")
    
    print("\n=== API Key Verification ===\n")
    
    openai_valid = verify_openai_key(openai_key)
    print("")
    hf_valid = verify_huggingface_key(hf_key)
    
    print("\n=== Summary ===")
    print(f"OpenAI API: {'✅ Valid' if openai_valid else '❌ Invalid'}")
    print(f"Hugging Face API: {'✅ Valid' if hf_valid else '❌ Invalid'}")
    
    if not openai_valid:
        print("\n⚠️ OpenAI API key is invalid. Please update it in the .env file.")
        sys.exit(1)
    else:
        print("\n✅ All necessary API keys are valid! You can run the load tests.")
        sys.exit(0) 