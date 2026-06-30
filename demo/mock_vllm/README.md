# Mock vLLM Server

## Overview
A lightweight server simulating vLLM streaming responses for local testing and debugging.

If you do not have a dedicated GPU / CUDA environment to run full vLLM models locally, but want to verify API interactions, WebUI flows, or CLI tooling, this utility serves as an instant drop-in replacement.

- Simulates OpenAI-compatible `/v1/chat/completions` and `/v1/models` streaming endpoints.
- Pure Python with zero heavy CUDA/vLLM library dependencies.
- Runs cross-platform on macOS, Linux, and Windows.

## Usage

Start the mock server on port 8000:

```bash
cd demo/mock_vllm
python3 start_mock_vllmserver.py
```

Then in separate terminals, start the API server and frontend interface (CLI or WebUI) to test end-to-end communication.
