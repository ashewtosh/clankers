import os
from pathlib import Path

_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"

def _load_env(path: Path) -> None:
    if not path.is_file():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))

_load_env(_ENV_FILE)

class Settings:
    def __init__(self) -> None:
        self.nim_api_key = os.getenv("NIM_API_KEY")
        self.nim_base_url = os.getenv("NIM_BASE_URL")
        self.nim_model = os.getenv("NIM_MODEL")