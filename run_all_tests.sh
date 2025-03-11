#!/bin/bash

# Run all load tests and generate reports
# Usage: ./run_all_tests.sh [duration] [users] [spawn_rate]

# Default values
DURATION=${1:-"1m"}  # Default: 1 minute
USERS=${2:-10}       # Default: 10 users
SPAWN_RATE=${3:-2}   # Default: 2 users per second

# Create reports directory if it doesn't exist
mkdir -p reports

# Ensure .env file exists
if [ ! -f .env ]; then
  echo "Error: .env file not found in the root directory."
  echo "Please create a .env file with your API keys. See README.md for details."
  exit 1
fi

echo "=== API Key Verification ==="
cd locustfiles
python verify_api_keys.py
VERIFY_STATUS=$?

if [ $VERIFY_STATUS -ne 0 ]; then
  echo "API key verification failed. Please fix the issues before running tests."
  exit 1
fi

echo ""
echo "=== Running OpenAI Load Test ==="
echo "Duration: $DURATION, Users: $USERS, Spawn Rate: $SPAWN_RATE"
locust -f openai_locustfile.py --headless -u $USERS -r $SPAWN_RATE -t $DURATION --html=../reports/openai_report.html --csv=../reports/openai

echo ""
echo "=== Running Hugging Face Load Test ==="
echo "Duration: $DURATION, Users: $USERS, Spawn Rate: $SPAWN_RATE"
locust -f huggingface_locustfile.py --headless -u $USERS -r $SPAWN_RATE -t $DURATION --html=../reports/huggingface_report.html --csv=../reports/huggingface

cd ..
echo ""
echo "=== Tests Completed ==="
echo "Reports are available in the reports directory:"
echo "- OpenAI Report: reports/openai_report.html"
echo "- Hugging Face Report: reports/huggingface_report.html"
echo ""
echo "CSV data is also available in the reports directory." 