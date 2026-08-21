import glob
import os
import subprocess
import time
from pathlib import Path

import requests
import runpod

MODEL_REPO = "HauhauCS/Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced"
MODEL_FILE = "Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf"
CACHE_ROOT = "/runpod-volume/huggingface-cache/hub"
PORT = 3098


def resolve_model() -> str:
    pattern = f"{CACHE_ROOT}/models--HauhauCS--Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced/snapshots/*/{MODEL_FILE}"
    matches = glob.glob(pattern)
    if not matches:
        raise RuntimeError(f"Cached model not found: {pattern}")
    return matches[0]


def start_server() -> subprocess.Popen:
    model = resolve_model()
    binary = os.environ.get("LLAMA_SERVER", "/usr/local/bin/llama-server")
    if not Path(binary).exists():
        binary = "/app/llama-server"
    process = subprocess.Popen([binary, "--model", model, "--host", "127.0.0.1", "--port", str(PORT), "--ctx-size", "4096", "-ngl", "999"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    for _ in range(600):
        if process.poll() is not None:
            raise RuntimeError("llama-server exited during startup")
        try:
            if requests.get(f"http://127.0.0.1:{PORT}/v1/models", timeout=1).ok:
                return process
        except requests.RequestException:
            pass
        time.sleep(1)
    process.kill()
    raise TimeoutError("llama-server startup timed out")


server = start_server()


def handler(job):
    payload = job.get("input", {})
    response = requests.post(f"http://127.0.0.1:{PORT}/v1/chat/completions", json=payload, timeout=900)
    response.raise_for_status()
    return response.json()


runpod.serverless.start({"handler": handler})
