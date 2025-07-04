import json

from LoadJson import LoadJson

# finds and sets correct headers for choosen server by the input url; also sets serverconfig
class ConfigHandler(LoadJson): # returns config related jsons
    def __init__(self, url: str):
        # loads and sets json configs
        super().__init__()
        self.__config: json = super().getConfig()
        self.__httpHeader: json = super().getHttpHeader()

        # sets server related configs
        self.setServerConfig(url)
        self.setServerHttpHeader()
        self.setCoverHttpHeader()

    def setServerConfig(self, url: str) -> None:
        status: bool = False # stays false if severconfig can not be found
        for item in self.__config:
            if str(item.get("server")) in url:
                self.__serverConfig: json = item
                status = True
                break
        if not status:
            print("<< Server config not found >>")
            exit()
        
    def setServerHttpHeader(self) -> None: # based on ServerConfig
        headerKey: str = self.__serverConfig["request"].get("header", "default") # json key of the httpHeader
        httpHeader: json = self.__httpHeader.get(headerKey)
        if headerKey and not httpHeader: # header not found and not default
            print("<< Configured request header not found >>")
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