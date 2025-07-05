# simple extension class for http errors
class HttpExpection(Exception):
    def __init__(self, status_code: int, message: str, adress: str):
        super().__init__(f"[HTTP {status_code}] Error - '{adress}' - *{message}*")