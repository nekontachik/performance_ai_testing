from locust import HttpUser, task, between
import json
import os
from dotenv import load_dotenv
import sys

# Add the parent directory to sys.path to allow importing from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)

class OpenAITestUser(HttpUser):
    wait_time = between(1, 3)
    
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it in the .env file in the root directory.")
        sys.exit(1)
    
    # Get model from environment variable or use default
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    host = "https://api.openai.com"

    @task(1)
    def chat_completion(self):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Use the chat completions endpoint
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Write a short description of API testing."}
            ],
            "max_tokens": 50
        }
        
        with self.client.post("/v1/chat/completions", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                error_detail = ""
                try:
                    error_detail = json.dumps(response.json())
                except:
                    error_detail = response.text[:100]
                response.failure(f"Status code: {response.status_code}, Error: {error_detail}")

if __name__ == "__main__":
    import os
    os.system("locust -f openai_locustfile.py")
