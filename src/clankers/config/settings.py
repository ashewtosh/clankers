import os

class Settings:
    def __init__(self) -> None:
        self.nim_api_key = os.getenv("NIM_API_KEY")
        self.nim_base_url = os.getenv("NIM_BASE_URL")
        self.nim_model = os.getenv("NIM_MODEL")