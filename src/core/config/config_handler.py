from src.core.config.load_json import LoadJson

# finds and sets correct headers for choosen server by the input url; also sets serverconfig
class ConfigHandler(LoadJson): # returns config related jsons
    def __init__(self, url: str):
        super().__init__()
        # loading json as dict
        self.__config: dict = super().getConfig()
        self.__httpHeader: dict = super().getHttpHeader()
        self.__url: str = url

    def get_server_config(self) -> None:
        for item in self.__config: # for in every server config
            if item.get("server") in self.__url:
                return item
        print("<< Server config not found >>")
        exit()
        
    def setServerHttpHeader(self) -> None: # based on ServerConfig
        headerKey: str = self.__serverConfig["request"].get("header") # sets header id if found
        
        self.__serverHttpHeader: json = self.__httpHeader.get(headerKey) # gets dict of header id
        if headerKey and not httpHeader: # header not found and not default
            httpHeader: json = self.__httpHeader.get("default")
        self.__serverHttpHeader = httpHeader

    # also based on ServerConfig["coverHeader"]
    def setCoverHttpHeader(self) -> None:
        headerKey: str = self.__serverConfig["request"].get("coverHeader", None)
        self.__coverHttpHeader: json = {}
        # specific header for cover sides not set
        if not headerKey: 
            self.__coverHttpHeader = self.__serverHttpHeader
        # headerKey is found for cover requests
        else: 
            httpHeader: json = self.__httpHeader.get(headerKey)
            # header not found -> coverHttpH = serverHttpH
            if not httpHeader: 
                self.__coverHttpHeader = self.__serverHttpHeader
            else:
                self.__coverHttpHeader = httpHeader

    def getServerConfig(self) -> json:
        return self.__serverConfig

    def getCoverHttpHeader(self) -> json:
        return self.__coverHttpHeader
            
    def getServerHttpHeader(self) -> json:
        return self.__serverHttpHeader