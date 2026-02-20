from app.utils import CONFIG

from app.service_clients import BaseAPIClient


class BaseOgcClient(BaseAPIClient):

    _host = CONFIG.config["OGC"]["HOST"]
    _timeout = CONFIG.config["OGC"]["TIMEOUT"]