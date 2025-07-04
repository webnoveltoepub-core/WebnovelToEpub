import requests

# for using cloudflare server (solve automated); returns request
class FlaresolverrClient:
    def __init__(self, flare_url: str = "http://localhost:8191/v1", session_id: str = None): # CHANGEME base_url get through conf
        self.__flare_url: str = flare_url
        self.__session_id: str = session_id
        
    # make request to flaresolverr server; getting html side in str format
    def get(self, url: str, http_header: dict[str,str] = None, max_timeout: int = 60000) -> str|None:
        # for flaresolverr
        payload: dict[str,str] = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": max_timeout
        }
        # passed session id; if not set cookies are not saved persistent
        if self.__session_id: 
            payload["session"] = self.__session_id
        # http_header is passed; use that instead of default of flaresolverr
        if http_header:
            payload["headers"] = http_header
        # requesting flaresolverr
        try:
            response: requests = requests.post(self.__flare_url, json = payload)
            status: int = response.raise_for_status()
            return response.json().get("solution", {}).get("response")
        # error while connecting to flaresolverr server
        except requests.RequestException as e:
            print(f"{status}: *{e}* - '{self.__flare_url}'")
            return None