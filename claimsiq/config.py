import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
DATA_OPERATIONS_ENABLED = os.getenv("ENABLE_DATA_OPERATIONS", "false").lower() in {"1", "true", "yes", "on"}
