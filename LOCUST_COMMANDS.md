# Locust Commands Quick Reference

This document provides a quick reference for common Locust commands used in this project.

## Basic Commands

### Start Locust with Web UI
```bash
cd locustfiles
locust -f openai_locustfile.py
```

### Start Locust without Web UI (Headless Mode)
```bash
locust -f openai_locustfile.py --headless -u 10 -r 1 -t 30s
```

### Run a Specific Test File
```bash
locust -f huggingface_locustfile.py
```

## Command Line Options

### User Control
- `-u, --users`: Number of concurrent users (default: 1)
- `-r, --spawn-rate`: Rate at which users are spawned (users per second, default: 1)
- `-t, --run-time`: Stop after the specified time (e.g., 300s, 20m, 3h)

### Web UI Options
- `--web-host`: Host for the web interface (default: 0.0.0.0)
- `--web-port`: Port for the web interface (default: 8089)
- `--headless`: Run without web UI

### Output Options
- `--html=FILE`: Generate HTML report after test
- `--csv=PREFIX`: Store test results in CSV files with the specified prefix
- `--log-level`: Set log level (DEBUG/INFO/WARNING/ERROR/CRITICAL)

## Examples

### Run a 5-minute Test with 50 Users
```bash
locust -f openai_locustfile.py --headless -u 50 -r 5 -t 5m
```

### Generate HTML Report
```bash
locust -f openai_locustfile.py --headless -u 10 -r 1 -t 1m --html=../reports/openai_report.html
```

### Run on a Different Port
```bash
locust -f openai_locustfile.py --web-port=8090
```

### Save Results to CSV
```bash
locust -f openai_locustfile.py --headless -u 20 -r 2 -t 2m --csv=../reports/openai_results
```

## Distributed Load Testing

### Start Master Node
```bash
locust -f openai_locustfile.py --master
```

### Start Worker Node
```bash
locust -f openai_locustfile.py --worker --master-host=localhost
```

### Start Master with Custom Options
```bash
locust -f openai_locustfile.py --master --expect-workers=4 --web-port=8089
```

## Environment Variables

You can use environment variables to configure Locust:

```bash
# Set number of users
export LOCUST_USERS=100

# Set spawn rate
export LOCUST_SPAWN_RATE=10

# Set run time
export LOCUST_RUN_TIME=10m

# Run with these settings
locust -f openai_locustfile.py --headless
```

## Custom Host

To specify a different host than the one defined in the locustfile:

```bash
locust -f openai_locustfile.py --host=https://api.alternate-openai-endpoint.com
```

## Stopping Tests

- In web UI: Click the "Stop" button
- In headless mode: Press Ctrl+C
- With time limit: Tests will stop automatically after the specified time 