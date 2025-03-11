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

class HuggingFaceAPITestUser(HttpUser):
    wait_time = between(1, 3)
    
    # Get API key from environment variable
    api_key = os.getenv("HF_API_KEY")
    
    # Get model from environment variable or use default
    model = os.getenv("HF_MODEL", "gpt2")
    
    # Determine if we should use the API or just browse the model page
    use_api = os.getenv("HF_USE_API", "false").lower() == "true"
    
    # Set the appropriate host based on whether we're using the API
    host = "https://api-inference.huggingface.co" if use_api else "https://huggingface.co"

    @task(1)
    def huggingface_request(self):
        if self.use_api and self.api_key:
            self.inference_api_request()
        else:
            self.browse_model_page()
    
    def inference_api_request(self):
        """Make a request to the Hugging Face Inference API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": "Write a short description of API testing."
        }
        
        endpoint = f"/pipeline/text-generation/{self.model}"
        
        with self.client.post(endpoint, json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                error_detail = ""
                try:
                    error_detail = json.dumps(response.json())
                except:
                    error_detail = response.text[:100]
                response.failure(f"Status code: {response.status_code}, Error: {error_detail}")
    
    def browse_model_page(self):
        """Browse the public model page on huggingface.co"""
        # Use a public URL that doesn't require authentication
        with self.client.get(f"/docs/transformers/model_doc/{self.model}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                error_detail = ""
                try:
                    error_detail = response.text[:100]
                except:
                    pass
                response.failure(f"Status code: {response.status_code}, Error: {error_detail}")

if __name__ == "__main__":
    import os
    os.system("locust -f huggingface_locustfile.py")
