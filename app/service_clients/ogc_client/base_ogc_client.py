from app.utils import CONFIG

from app.service_clients import BaseAPIClient


class BaseOgcClient(BaseAPIClient):
    _host = CONFIG.config["OGC"]["HOST"]
    _timeout = CONFIG.config["OGC"]["TIMEOUT"]

    @classmethod
    def prepare_headers(cls, **extra):
        headers = super().prepare_headers(**extra)
        auth_token = CONFIG.config.get("OGC", {}).get("AUTH_TOKEN")
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        return headers