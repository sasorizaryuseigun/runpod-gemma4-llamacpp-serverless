# RunPod Gemma4 llama.cpp Serverless

RunPod Serverless worker using llama.cpp and the RunPod Hugging Face model cache.

The worker expects the endpoint model reference to be:

`https://huggingface.co/HauhauCS/Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced:main`

It explicitly loads `Gemma4-26B-A4B-Uncensored-HauhauCS-Balanced-Q4_K_M.gguf` from the cached snapshot and serves OpenAI-compatible chat completions through the RunPod Serverless endpoint.
