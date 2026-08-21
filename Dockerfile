FROM nvidia/cuda:12.8.1-devel-ubuntu24.04 AS build
RUN apt-get update && apt-get install -y --no-install-recommends git cmake build-essential ca-certificates && rm -rf /var/lib/apt/lists/*
RUN git clone --depth 1 https://github.com/ggml-org/llama.cpp.git /src/llama.cpp
WORKDIR /src/llama.cpp
RUN cmake -B build -DGGML_CUDA=ON -DGGML_NATIVE=OFF -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release -j$(nproc) --target llama-server

FROM nvidia/cuda:12.8.1-runtime-ubuntu24.04
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=build /src/llama.cpp/build/bin/llama-server /usr/local/bin/llama-server
RUN pip3 install --break-system-packages runpod requests
COPY handler.py /app/handler.py
WORKDIR /app
CMD ["python3", "handler.py"]
