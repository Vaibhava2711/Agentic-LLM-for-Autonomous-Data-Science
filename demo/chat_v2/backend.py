import uvicorn

from backend_app.app import app
from backend_app.settings import settings


if __name__ == "__main__":
    print("Starting backend services...")
    print(f"   - API Service: http://localhost:{settings.backend_port}")
    print(f"   - File Service: {settings.file_server_base}")
    uvicorn.run(app, host=settings.backend_host, port=settings.backend_port)
