# Chatty

A small bot that periodically sends chat completion requests to a Nutanix AI (or OpenAI-compatible) endpoint. Useful for basic load testing on an endpoint.

## Install

```bash
git clone <repository-url>
cd chatty
pip install -r requirements.txt
```

Or install dependencies in a virtual environment:

```bash
git clone <repository-url>
cd chatty
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

All three options are required. If any is missing, the script prints a help screen and exits.

| Option     | Description |
|-----------|-------------|
| `--url`   | Base URL of the API (e.g. `https://nai.example.com/enterpriseai/v1/`) |
| `--model` | Model name (e.g. `llama-instruct`) |
| `--token` | API token for the endpoint |

**Example:**

```bash
python chatty-bot.py \
  --url https://ai.example.com/enterpriseai/v1/ \
  --model llama-instruct \
  --token aaa-bbb-ccc-ddd-eee
```

**Help:**

```bash
python chatty-bot.py --help
```

On startup, the script tests the endpoint once. If the test succeeds, it prints how to exit and then runs the main loop. To stop the bot, press **Ctrl+C**.
