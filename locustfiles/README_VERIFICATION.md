# API Key Verification Tool

This tool helps you verify that your API keys for OpenAI and Hugging Face are valid before running load tests.

## Usage

```bash
python verify_api_keys.py
```

## How It Works

The verification script:

1. Extracts API keys from your locustfiles
2. Makes a minimal API request to each service
3. Reports whether the keys are valid or not
4. Provides detailed error information if a key is invalid

## Example Output

```
=== API Key Verification ===

Testing OpenAI API key...
✅ OpenAI API key is valid!

Testing Hugging Face API key...
❌ Hugging Face API key error
Error details: {"error":"Your auth method doesn't allow you to make inference requests"}

=== Summary ===
OpenAI API: ✅ Valid
Hugging Face API: ❌ Invalid

⚠️ Some API keys are invalid. Please update them in the locustfiles.
```

## Troubleshooting

### OpenAI API Key Issues

If your OpenAI API key is invalid, you might see:

- `"error": "invalid_api_key"` - The API key is malformed or doesn't exist
- `"error": "insufficient_quota"` - You've exceeded your usage limits
- `"error": "access_terminated"` - Your account access has been terminated

Solutions:
1. Generate a new API key in the [OpenAI dashboard](https://platform.openai.com/api-keys)
2. Check your usage limits and billing status
3. Ensure you're using the correct key format (starts with "sk-")

### Hugging Face API Key Issues

If your Hugging Face API key is invalid, you might see:

- `"error": "Authorization header is invalid"` - The API key is malformed
- `"error": "Your auth method doesn't allow you to make inference requests"` - Insufficient permissions

Solutions:
1. Generate a new API key in the [Hugging Face settings](https://huggingface.co/settings/tokens)
2. Ensure your account has access to the Inference API
3. Check that you're using the correct key format (starts with "hf_")

## Using Environment Variables

You can also use environment variables for your API keys:

```bash
export OPENAI_API_KEY="your-api-key"
export HF_API_KEY="your-huggingface-key"
python verify_api_keys.py --use-env
```

To enable this, modify the script to accept command line arguments:

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--use-env", action="store_true", help="Use environment variables for API keys")
args = parser.parse_args()

if args.use_env:
    import os
    openai_key = os.environ.get("OPENAI_API_KEY")
    hf_key = os.environ.get("HF_API_KEY")
```

## Extending the Script

You can extend this script to verify other API keys by adding new verification functions:

```python
def verify_anthropic_key(api_key):
    print("Testing Anthropic API key...")
    # Implementation here
    return True/False
``` 