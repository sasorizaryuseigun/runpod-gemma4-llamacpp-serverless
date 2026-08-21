FROM nvidia/cuda:12.8.1-runtime-ubuntu24.04

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates python3 python3-pip tar && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://github.com/ggml-org/llama.cpp/releases/download/b10545/llama-b10545-bin-ubuntu-x64.tar.gz -o /tmp/llama.tar.gz \
    && mkdir -p /tmp/llama \
    && tar -xzf /tmp/llama.tar.gz -C /tmp/llama \
    && install -m 0755 /tmp/llama/llama-server /usr/local/bin/llama-server \
    && rm -rf /tmp/llama /tmp/llama.tar.gz
RUN pip3 install --break-system-packages runpod requests
COPY handler.py /app/handler.py
WORKDIR /app
CMD ["python3", "handler.py"]
