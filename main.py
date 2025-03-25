import logging
import uvicorn
from src.app import app

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
