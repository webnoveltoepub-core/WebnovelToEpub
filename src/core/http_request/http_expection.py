# simple extension class for http errors
class HttpExpection(Exception):
    def __init__(self, status_code: int, message: str, adress: str):
        # public attributes to manually check up
        self.status_code: int = status_code
        self.message: str = message
        self.adress: str = adress

        super().__init__(f"[HTTP {status_code}] Error - '{adress}', *{message}*")