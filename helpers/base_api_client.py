import requests


class BaseApiClient(object):
    API_NAME = None
    BASE_API_URL = None
    HOST = None
    KEY = None

    def __init__(self):
        self.host = self.HOST
        self.base_url = self.BASE_API_URL.format(self.host)
        self.key = self.KEY

    def _get_headers(self):
        return {"Content-Type": "application/json"}

    def _request(self, request_method: str, url: str, payload=None):
        if request_method == "get":
            return requests.get(url, headers=self._get_headers())
        if request_method == "post":
            return requests.post(url, headers=self._get_headers(), json=payload)

    def get(self, url, **kwargs):
        page_number = kwargs.get("page_number", 0)
        page_size = kwargs.get("page_size", 100)
        return self._request("get", "{}/?&page-number={}&page-size={}&key={}".format(
            url, page_number, page_size, self.key
        ))

    def post(self, url, payload):
        return self._request("post", "{}/?&key={}".format(url, self.key), payload)
