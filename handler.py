import glob
import os
import subprocess
import time

import requests
import runpod

MODEL_FILE = "Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf"
CACHE_ROOT = "/runpod-volume/huggingface-cache/hub"
PORT = 3098


def resolve_model():
    pattern = f"{CACHE_ROOT}/models--HauhauCS--Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced/snapshots/*/{MODEL_FILE}"
    matches = glob.glob(pattern)
    if not matches:
        raise RuntimeError(f"Cached model not found: {pattern}")
    return matches[0]


def wait_for_server(process):
    for _ in range(900):
        if process.poll() is not None:
            raise RuntimeError("llama-server exited during startup")
        try:
            response = requests.get(f"http://127.0.0.1:{PORT}/v1/models", timeout=2)
            if response.ok and response.json().get("data"):
                return
        except (requests.RequestException, ValueError):
            pass
        time.sleep(1)
    process.kill()
    raise TimeoutError("llama-server startup timed out")


model_path = resolve_model()
server = subprocess.Popen([
    "/usr/local/bin/llama-server",
    "--model", model_path,
    "--host", "127.0.0.1",
    "--port", str(PORT),
    "--ctx-size", os.getenv("LLAMA_CTX_SIZE", "4096"),
    "-ngl", "999",
], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
wait_for_server(server)


def handler(job):
    payload = job.get("input", {})
    response = requests.post(
        f"http://127.0.0.1:{PORT}/v1/chat/completions",
        json=payload,
        timeout=900,
    )
    response.raise_for_status()
    return response.json()


runpod.serverless.start({"handler": handler})
