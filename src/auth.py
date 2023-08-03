from base64 import b64encode


from pydantic import BaseModel


class DanbooruAuth(BaseModel):
    username: str
    api_key: str

    def basic_auth(self) -> str:
        return b64encode(f"{self.username}:{self.api_key}".encode("utf-8")).decode(
            "utf-8"
        )

    def get_headers(self) -> dict[str, str]:
        headers = {"User-Agent": "MiniBooru Scraper"}
        headers["Authorization"] = f"Basic {self.basic_auth()}"
        return headers
