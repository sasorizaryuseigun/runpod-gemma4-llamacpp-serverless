# RunPod Gemma4 llama.cpp Serverless

Custom CUDA llama.cpp worker for RunPod Serverless. It uses RunPod's host-side Hugging Face cache and explicitly loads `Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf` from the cached snapshot.

Model reference:

`https://huggingface.co/HauhauCS/Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced:main`

The RunPod job input is forwarded to llama.cpp's OpenAI-compatible `/v1/chat/completions` endpoint.
