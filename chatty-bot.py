import argparse
import sys
import time
import random
from openai import OpenAI

def ParseArgs():
    parser = argparse.ArgumentParser(
        description="Chatty bot: periodic chat completions against an NAI endpoint."
    )
    parser.add_argument("--url", required=True, help="Base URL (e.g. https://nai.ntnxdemos.com/enterpriseai/v1/)")
    parser.add_argument("--model", required=True, help="Model name (e.g. llama-instruct-rcc)")
    parser.add_argument("--token", required=True, help="API token for the endpoint")
    return parser.parse_args()

def TestEndpoint(client, modelName):
    """Silent test of the endpoint. Raises on failure."""
    client.chat.completions.create(
        model=modelName,
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=1,
    )

def Main():
    args = ParseArgs()
    client = OpenAI(base_url=args.url, api_key=args.token)
    try:
        TestEndpoint(client, args.model)
    except Exception as e:
        err = str(e).lower()
        if "connection" in err or "refused" in err or "resolve" in err or "timeout" in err:
            print("Error: Could not reach the endpoint. Check --url and network.", file=sys.stderr)
        elif "401" in err or "unauthorized" in err or "authentication" in err:
            print("Error: Authentication failed. Check --token.", file=sys.stderr)
        elif "404" in err or "not found" in err:
            print("Error: Model or path not found. Check --url and --model.", file=sys.stderr)
        elif "429" in err or "rate" in err:
            print("Error: Rate limited. Try again later.", file=sys.stderr)
        elif "500" in err or "502" in err or "503" in err:
            print("Error: Server error. The endpoint may be unavailable.", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    print("Endpoint OK. Exit anytime with Ctrl+C.")

    prompt = "Briefly describe an interesting fact about technology in less than 100 words."
    count = 0
    while True:
        response = client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        count += 1
        print(f"Response {count}: {response.choices[0].message.content}")
        print("--------------------------------")
        timeList = [60, 120, 180, 240, 300, 360, 420, 480, 540, 600]
        randomTime = random.choice(timeList)
        print(f"Sleeping for {randomTime/60} minutes")
        time.sleep(randomTime)


if __name__ == "__main__":
    Main()
