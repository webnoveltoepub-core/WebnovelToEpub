from bs4 import BeautifulSoup
import requests
import json
import re

from FetchChapterList import FetchChapterList
from HTMLSearch import HTMLSearch

# uses FetchChapterLists url to the list of chapters(without paging), modifies it(add pages if possible) and fetches the chapterurls
class FetchChapterURLs(FetchChapterList):
    def __init__(self, httpRequest: requests, requestConfig: json, typeServer: bool, url: str, debug: bool, debughtml: bool):
        super().__init__(requestConfig, typeServer, url)
        self.__chapterListURL = super().getChapterListURL()
        self.__debug = debug # sets attribute for debugmode
        self.__debughtml = debughtml # sets visibity of html code when debugmode is enabled
        if self.__debug:
            print(f"<< generated base url leading to chapterlist:{self.__chapterListURL} -DEBUGMODE- >>")
        self.__requestConfig = requestConfig
        self.__httpRequest = httpRequest
        self.__chapterURLs: list[str] = []
        self.__HTMLpraser = HTMLSearch() 
        self.setChapterURLs()

    # will be executed by self.setChapterURLs to get the urls within chapterlist
    def fetchChapterURLs(self, response: requests) -> list[str]: # fetches the urls out of the chapterlist page/s
        patternChapterList = self.__requestConfig["pattern"]["chapterlist"]
        soup = BeautifulSoup(response.content, "html.parser")
        self.__HTMLpraser.setSoup(soup)
        
        # get section
        classHtml: str = patternChapterList.get("class", None)
        idHtml: str = patternChapterList.get("id", None)
        if classHtml or idHtml:
            self.__HTMLpraser.searchSection(classHtml, idHtml)
            if self.__debug:
                print(f"<< classHtml:{classHtml}, idHtml:{idHtml} -DEBUGMODE- proceed with printing soup ... >>")
                if self.__debughtml:
                    self.__HTMLpraser.returnSoup()
            
        # find elements (within section)
        tagHtml: str = patternChapterList.get("tag", "a")
        tagClassHtml: str = patternChapterList.get("tagClass", None)
        tagIdHtml: str = patternChapterList.get("tagId", None)
        if tagHtml or tagClassHtml or tagIdHtml:
            self.__HTMLpraser.searchElements(tagHtml, tagClassHtml, tagIdHtml)
            if self.__debug:
                print(f"<< tagHtml:{tagHtml}, tagClassHtml:{tagClassHtml}, tagIdHtml:{tagIdHtml} -CONFIG- -DEBUGMODE- proceed with printing soup ... >>")
                if self.__debughtml:
                    self.__HTMLpraser.returnSoup()
        
        # other patterns
        attribute: str = patternChapterList.get("attribute", "href")
        prefix: str = patternChapterList.get("prefix", "")
        suffix: str = patternChapterList.get("suffix", "")
        urlPattern: str = patternChapterList.get("urlPattern", None)

        # find_all -> list format
        chapterURLs: list[str] = []
        elements = self.__HTMLpraser.getSoup()
        for element in elements: # one element = one link
            if urlPattern:
                if not re.search(urlPattern, element):
                   continue
            attributeValue = element.get(attribute)
            chapterURL: str = prefix + attributeValue + suffix
            chapterURLs.append(chapterURL)
            if self.__debug:
                print(f"<< chapter url [{chapterURL}] fetched and added to list of chapter urls -CONFIG- -DEBUGMODE- >>")
        return chapterURLs

    def setChapterURLs(self) -> None:
        # creates instance for b4s
        paramPage: str = self.__requestConfig["params"].get("page", False)  # sets if only one chapterlist or more
        chapterListURL: str = self.__chapterListURL
        if self.__debug:
            print(f"<< chapterlist page setting:{paramPage} -CONFIG- -DEBUGMODE- >>")
        if paramPage: # if page is set
            paramPageStart: int = self.__requestConfig["params"].get("pageStart", 0) # sets the first page number (PAGE=0)
            x: int = paramPageStart
            while (True):
                chapterListURLPage = chapterListURL + paramPage + str(x) # link to one of many chapterlists
                if self.__debug:
                    print(f"<< proceed with fetching process of chapterlist page [{chapterListURLPage}] -DEBUGMODE- >>")
                response = self.__httpRequest.makeRequest(chapterListURLPage)
                if isinstance(response, int): # checks if errors did happen
                    if response == 404: # not reachable -> expection: last list passed
                        print("<< RequestError -404- is a common expection here and can be ignored normally >>")
                        break
                    else: # repeat with same chapterlist page expection: timeout
                        continue
                else:
                    pageChapterURLs: list[str] = self.fetchChapterURLs(response)
                    if len(pageChapterURLs) == 0: # contains no links -> expection: only empty lists are remaining
                        break
                    self.__chapterURLs.extend(pageChapterURLs)
                    if self.__debug:
                        print(f"<< successfully added chapter urls out of chapterlist [{chapterListURLPage}] -DEBUGMODE- >>")
                x += 1 # goes to the next page
        else: # page is not set
            while True: # repeats same url for timeout cases until successful
                if self.__debug:
                    print(f"<< proceed with fetching process of chapterlist [{chapterListURL}] -DEBUGMODE- >>")
                response = self.__httpRequest.makeRequest(chapterListURL)
                if isinstance(response, int):
                    if response == 404: # not reachable -> expection: only chapterlist not reachable
                        print(f"<< RequestError -404- only chapterlist not reachable [{chapterListURL}] >>")
                        exit()
                    else: # repeat with same chapterlist page expection: timeout
                        continue
                else:
                    chapterURLs: list[str] = self.fetchChapterURLs(response)                    
                    self.__chapterURLs = chapterURLs
                    if self.__debug:
                        print(f"<< successfully added chapter urls out of chapterlist [{chapterListURL}] -DEBUGMODE- >>")
                    break

    # returns fetched(by setChapterURLs) chapterUrls
    def getChapterURLs(self) -> list[str]:
        return self.__chapterURLs