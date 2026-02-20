from app.service_clients.ogc_client.base_ogc_client import BaseOgcClient
from app.service_clients import BaseAPIClient
from app.exceptions import BaseException


class OgcApiClient(BaseOgcClient):

    @classmethod
    @BaseAPIClient.api_handler()
    async def example(cls, data) -> dict:
        try:
            path = "/posts"
            payload = {
                "key": data
            }
            response = await cls.post(path=path, data=payload)
            return response.json()
        except BaseException:
            return {}

