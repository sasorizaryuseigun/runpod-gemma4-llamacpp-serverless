FROM nvidia/cuda:12.8.1-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y --no-install-recommends curl python3 python3-pip ca-certificates && rm -rf /var/lib/apt/lists/*
RUN curl -L https://github.com/ggml-org/llama.cpp/releases/download/b બને/llama-bબ-linux-cuda-12.8-x64.tar.gz -o /tmp/llama.tar.gz || true
RUN pip3 install --break-system-packages runpod openai
COPY handler.py /app/handler.py
WORKDIR /app
CMD ["python3", "handler.py"]
