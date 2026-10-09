import httpx
import json
import sys
def ollama_prompt_buffer(url, prompt, model):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = httpx.post(url, json=payload, timeout=None)
        if response.status_code == 200:
            return response.json().get("response", "")
        elif response.status_code == 404:
            print("[ERROR] 404 bad request or model does not exist!")
        else:
            print(f"[ERROR]: {response.status_code}")
    except httpx.RequestError as err:
        print(f"[ERROR!] : {err}")
    return None

def ollama_prompt_stream(url, prompt, model):
    if not isinstance(url, str) or not isinstance(prompt, str):
        raise TypeError("URL and prompt must both be of type str!")
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True
    }

    with httpx.Client(timeout=None) as Client:
        try:
            with Client.stream("POST", url, json=payload) as response:
                if response.status_code == 200:
                    pass
                elif response.status_code == 404:
                    print("[ERROR] 404 bad request! Are you sure the model youre requesting exists or if the url is correct?")

                response.raise_for_status()

                for line in response.iter_lines():
                    chunck = json.loads(line)
                    yield chunck.get("response", "")
        except httpx.RequestError as err:
            print(f"[ERROR] {err}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("[USAGE] : python3 <name>.py [buffer] [stream]")
        raise SystemExit
    if sys.argv[1] == 'stream':
        for text_fragment in ollama_prompt_stream("http://localhost:11434/api/generate", "generate a summary of the hashcat tool", "qwen1.5b"):
            print(text_fragment, end="", flush=True)
        print()
    elif sys.argv[1] == 'buffer':
        print(ollama_prompt_buffer("http://localhost:11434/api/generate", "generate a summary of the Ghidra tool.", "qwen1.5b"))
