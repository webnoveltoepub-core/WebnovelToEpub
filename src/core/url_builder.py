from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class URLBuilder:
    def __init__(self, url: str):
        self.__parsed = urlparse(url)
        self.__query = parse_qs(self.__parsed.query)

    def set_path(self, path: str):
        self.__parsed = self.__parsed._replace(path=path)
        return self

    def add_param(self, key: str, value: str):
        self.__query[key] = [value]
        return self

    def add_params(self, params: dict):
        for k, v in params.items():
            self.__query[k] = [v]
        return self

    def remove_param(self, key: str):
        self.__query.pop(key, None)
        return self

    def build(self) -> str:
        query_string = urlencode(self.__query, doseq=True)
        self.__parsed = self.__parsed._replace(query=query_string)
        return urlunparse(self.__parsed)