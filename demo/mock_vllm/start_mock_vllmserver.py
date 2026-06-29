import http.server
import json
import time
from typing import Dict, Any

# Mock assistant response text (streamed character-by-character)
FULL_RESPONSE_TEXT = """<Analyze>
To analyze the provided sales dataset, we need to inspect the monthly revenue figures and calculate the quarterly growth rate.
</Analyze>
<Code>
```python
import pandas as pd
df = pd.DataFrame({
    'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
    'Revenue ($k)': [1250, 1180, 1420, 1690]
})
growth = df['Revenue ($k)'].pct_change() * 100
print(df)
```
</Code>
<Execute>
```
  Quarter  Revenue ($k)
0      Q1          1250
1      Q2          1180
2      Q3          1420
3      Q4          1690
```
</Execute>
<Answer>
### Comprehensive Sales Trend Analysis:
1. **Q1 Revenue**: Strong start with $1,250k.
2. **Q2 Variance**: Minor seasonal contraction (-5.6%) down to $1,180k.
3. **H2 Acceleration**: Substantial rebound in Q3 ($1,420k) and annual peak in Q4 ($1,690k).
4. **Summary**: Overall full-year trajectory reflects a healthy 35.2% annualized expansion.
</Answer>"""

# Mock generated files
GENERATED_FILES = [
    {
        "name": "sales_trend.png",
        "url": "http://localhost:8100/generated/sales_trend.png"
    }
]

class VLLMHandler(http.server.BaseHTTPRequestHandler):
    # Disable default access logging
    def log_message(self, format, *args):
        return

    def _send_sse_response(self):
        """Send character-by-character SSE streaming response."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        chunk_id = f"chatcmpl-{int(time.time() * 1000)}"
        created_time = int(time.time())
        model = "DeepAnalyze-8B"

        char_list = list(FULL_RESPONSE_TEXT)
        for char in char_list:
            chunk = {
                "id": chunk_id,
                "object": "chat.completion.chunk",
                "created": created_time,
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": char},
                        "finish_reason": None
                    }
                ]
            }
            sse_line = f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
            self.wfile.write(sse_line.encode("utf-8"))
            self.wfile.flush()
            time.sleep(0.01)

        # Send final chunk
        final_chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": created_time,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {},
                    "finish_reason": "stop"
                }
            ],
            "generated_files": GENERATED_FILES
        }
        final_sse_line = f"data: {json.dumps(final_chunk, ensure_ascii=False)}\n\n"
        self.wfile.write(final_sse_line.encode("utf-8"))
        self.wfile.flush()

        # Send SSE DONE marker
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()

    def _send_json_response(self, status_code: int, content: Dict[str, Any]):
        """Send non-streaming JSON response."""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(content, ensure_ascii=False).encode("utf-8"))

    def do_POST(self) -> None:
        """Handle POST request."""
        if self.path == "/v1/chat/completions":
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                request_body = self.rfile.read(content_length).decode('utf-8')
                request_data = json.loads(request_body)
                stream = request_data.get('stream', False)

                if stream:
                    self._send_sse_response()
                else:
                    # Non-streaming return full response
                    full_response = {
                        "id": f"chatcmpl-{int(time.time() * 1000)}",
                        "object": "chat.completion",
                        "created": int(time.time()),
                        "model": "DeepAnalyze-8B",
                        "choices": [
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": FULL_RESPONSE_TEXT,
                                    "files": GENERATED_FILES
                                },
                                "finish_reason": "stop"
                            }
                        ],
                        "generated_files": GENERATED_FILES
                    }
                    self._send_json_response(200, full_response)

            except Exception as e:
                self._send_json_response(500, {"error": str(e)})

        elif self.path == "/v1/models":
            models_response = {
                "object": "list",
                "data": [
                    {
                        "id": "DeepAnalyze-8B",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "deepanalyze"
                    }
                ]
            }
            self._send_json_response(200, models_response)

        else:
            self._send_json_response(404, {"error": "Endpoint not found"})

    def do_GET(self) -> None:
        """Handle GET request."""
        if self.path == "/health":
            self._send_json_response(200, {"status": "healthy", "timestamp": int(time.time())})
        elif self.path == "/v1/models":
            self.do_POST()
        else:
            self._send_json_response(404, {"error": "Endpoint not found"})

def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Start mock vLLM server."""
    server = http.server.ThreadingHTTPServer((host, port), VLLMHandler)
    print(f"✅ Mock vLLM server started successfully (streaming)")
    print(f"   - Address: http://{host}:{port}")
    print(f"   - Press Ctrl+C to stop server\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server.shutdown()
        server.server_close()
        print("✅ Server stopped")

if __name__ == "__main__":

    run_server(host="0.0.0.0", port=8000)
