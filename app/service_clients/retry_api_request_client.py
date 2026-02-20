from app.constants import HttpStatusCodes
from app.exceptions.base_exception import BaseException

class RetryApiRequestClient:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    async def call_api(self, api_function, *args, **kwargs):
        for attempt in range(self.max_retries):
            try:
                return await api_function(*args, **kwargs)
            except BaseException as e:
                if(attempt < (self.max_retries - 1)) and ((e.status_code == HttpStatusCodes.REQUEST_TIMEOUT.value) or (e.status_code > HttpStatusCodes.INTERNAL_SERVER_ERROR.value)):
                    continue
                raise e