import requests

from src.core.http_request.http_expection import HttpExpection

# for using cloudflare server (solve automated); returns request
class FlaresolverrClient:
    def __init__(self, flare_url: str = "http://localhost:8193/v1", session_id: str = None): # CHANGEME base_url get through conf
        self.__flare_url: str = flare_url
        self.__session_id: str = session_id
        self.__cmd: str = "request.get"

    # make request to flaresolverr server; getting html side in str format
    def get(self, url: str, http_header: dict[str, str] = None) -> str | None:
        # for flaresolverr
        payload: dict[str, str] = {
            "cmd": self.__cmd,
            "url": url,
            "maxTimeout": 60000 # in millisec
        }

        # requesting external side
        if url:
            payload["url"] = url
        # passed session id; if not set cookies are not saved persistent
        if self.__session_id: 
            payload["session"] = self.__session_id
        # http_header is passed; use that instead of default of flaresolverr
        if http_header:
            payload["headers"] = http_header

        # requesting flaresolverr
        try:
            response = requests.post(self.__flare_url, json = payload)
            response.raise_for_status()
            data: dict = response.json()

            # flaresolverr connection successfully; check response from flaresolverr errors
            flare_status_code: int = data.get("solution", {}).get("status", 500)
            if flare_status_code != 200: # flaresolverr  
                message: str = data.get("message", "no message")
                raise HttpExpection(flare_status_code, message, url)
                
            return response.json().get("solution", {}).get("response") # returns html page
        # error while connecting to flaresolverr server
        except requests.RequestException as e:
            status_code: int = 500
            if hasattr(e, "response") and e.response is not None:
                status_code = e.response.status_code
            raise HttpExpection(status_code, e, self.__flare_url)

    # remove session id from flaresolverr
    def __del__(self):
        # if session_id is used; destroy session
        if self.__session_id:
            self.__cmd = "sessions.destroy"
            self.get()