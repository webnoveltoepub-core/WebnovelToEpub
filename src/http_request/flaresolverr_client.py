import requests

# for using cloudflare server (solve automated); returns request
class FlaresolverrClient:
    def __init__(self, flare_url: str = "http://localhost:8191/v1", session_id: str = None): # CHANGEME base_url get through conf
        self.__flare_url: str = flare_url
        self.__session_id: str = session_id
        self.__cmd: str = "request.get"

    # make request to flaresolverr server; getting html side in str format
    def get(self, url: None, http_header: dict[str, str] = None) -> str|None:
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
            response: requests = requests.post(self.__flare_url, json = payload)
            response.raise_for_status()
            return response.json().get("solution", {}).get("response")
        # error while connecting to flaresolverr server
        except requests.RequestException as e:
            print(f"{e.response.status_code}: *{e}* - '{self.__flare_url}'")
            return None
        
    # remove session id from flaresolverr
    def __del__(self):
        # if session_id is used; destroy session
        if self.__session_id:
            self.__cmd = "sessions.destroy"
            self.get()