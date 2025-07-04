import json

# creates a basic url to the chapterlist that containtes the chapterurls(without paging) and doesn't make any *request*
# creates url to chapter page (where the chapter urls are listed); if more then one it will be modified by ChapterURLs
class ChapterPageURL:
    def __init__(self, requestConfig: json, typeServer: bool, url: str):
        self.__requestConfig = requestConfig
        self.__typeServer = typeServer
        self.__url = url
        
        # generating base url for external or internal requests
        self.setChapterListURL()
    
    # filter: value -> filters the book id out of the given url
    def getBookId(self) -> str:
        # sets variables for fetching the id value
        filter: str = self.__requestConfig.get("filter")
        url: str = self.__url
        # parts that will be deleted from the input url
        filterPatterns: list[str] = filter.split("{}")
        # deletes all around but the id value
        removeBegin: str = url.replace(filterPatterns[0], "") # deletes before the brachets
        splitEnd: list[str] = removeBegin.split(filterPatterns[1])
        bookId: str = splitEnd[0]
        return bookId
    
    # sets urls that contains the chapterurls but without page ending(will be added by FetchChapterURLs.py)
    def setChapterListURL(self) -> str: # is the base for the url to chapterlist
        urlBase: str = self.__requestConfig.get("url", None)
        # typeServer = True; url: https://test.html?id=bookid
        if self.__typeServer is True:
            urlBase += "?"
            # adds id param for chosen book ?id=id
            if "id" in self.__requestConfig["params"]:
                idParam: str = f"{self.__requestConfig["params"].get("id")}={self.getBookId()}"
                urlBase += f"{idParam}&"
                
            # for common additional keys
            keys = ["add"]
            for key in keys: # adds basic parameters
                if key in self.__requestConfig["params"]:
                    urlBase += f"{self.__requestConfig["params"].get(key)}&"
                
        # typeServer = False; url: https://test/{bookid}.html
        elif self.__typeServer is False:
            urlBase = urlBase.replace("{}", self.getBookId()) # puts bookId into needed url /id/

        # deletes symbols on the end of the url that are not needed (& or ?)
        if urlBase.endswith("&") or urlBase.endswith("?"):
            urlBase = urlBase[:-1]
        # sets new chapterListURL
        self.__chapterListURL: str = urlBase
        
    def getChapterListURL(self) -> str:
        return self.__chapterListURL