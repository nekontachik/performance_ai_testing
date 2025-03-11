# Locust Test Files

This directory contains the Locust test files for different AI APIs.

## Files

- `openai_locustfile.py` - Load test for OpenAI API
- `huggingface_locustfile.py` - Load test for Hugging Face API
- `verify_api_keys.py` - Script to verify API keys before running tests
- `README_VERIFICATION.md` - Documentation for the API key verification process

## Running Tests

### OpenAI API

To test the OpenAI API:

```bash
cd locustfiles
python openai_locustfile.py
```

This will start the Locust web interface at http://localhost:8089.

### Hugging Face API

To test the Hugging Face API:

```bash
cd locustfiles
python huggingface_locustfile.py
```

This will start the Locust web interface at http://localhost:8089 (or another port if 8089 is already in use).

## Headless Mode

You can also run tests without the web interface:

```bash
cd locustfiles
locust -f openai_locustfile.py --headless -u 10 -r 1 -t 30s
```

Where:
- `-u 10` - Simulates 10 users
- `-r 1` - Spawns 1 user per second
- `-t 30s` - Runs the test for 30 seconds

## Generating Reports

To generate HTML reports:

```bash
cd locustfiles
locust -f openai_locustfile.py --headless -u 10 -r 1 -t 1m --html=../reports/openai_report.html
```

This will create a report in the `reports/` directory. 