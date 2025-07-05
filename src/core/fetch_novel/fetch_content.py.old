from bs4 import BeautifulSoup
import requests
import json

from Requests.HTMLSearch import HTMLSearch

# fetches chapter content(title and paragraphes of chapter) within each returned conent based on chapterurl(fetched by fetchChapterURLs)
# pass return of chapter requests here; gets chapter content (lines of text) and it's chapter title
class FetchContent:
    def __init__(self, httpRequest: requests, requestConfig: json):
        self.__httpRequest = httpRequest # same object and session of "httpRequest" given by "main.py"
        self.__requestConfig = requestConfig
        self.__HTMLpraser = HTMLSearch()

    # makes a request to needed chapter url and sets attribute
    def setChapter(self, chapterURL: str) -> None:
        while True: # repeats same url for timeout cases until successful
            response = self.__httpRequest.makeRequest(chapterURL)
            if isinstance(response, int):
                if response == 404: # not expected error
                    exit()
            else: # request was successfull
                self.__chapter: requests = response
                break

    # sets default values if not setted within the configs
    def setDefaultTag(self, tag) -> None:
        self.__defaultTag: str = tag
        
    # base search through the needed pages (call by getChapterTitle and getChapterContent)
    def fetchChapter(self, pattern: str) -> BeautifulSoup:
        soup: BeautifulSoup = BeautifulSoup(self.__chapter.content, "html.parser")
        self.__HTMLpraser.setSoup(soup)
        patternContent: json = self.__requestConfig["pattern"][pattern] # releated if title or content is needed
        # get section
        classHtml: str = patternContent.get("class", None)
        idHtml: str = patternContent.get("id", None)
        if classHtml or idHtml:
            self.__HTMLpraser.searchSection(classHtml, idHtml)
            
        # find elements (within section)
        tagHtml: str = patternContent.get("tag", self.__defaultTag)
        tagClassHtml: str = patternContent.get("tagClass", None)
        tagIdHtml: str = patternContent.get("tagId", None)
        if tagHtml or tagClassHtml or tagIdHtml:
            self.__HTMLpraser.searchElements(tagHtml, tagClassHtml, tagIdHtml)
        
    def getTitle(self) -> str: # returns without tags as string
        self.setDefaultTag(None)
        self.fetchChapter("chaptertitle") # fetches the title of the chapter
        attribute = self.__requestConfig["pattern"]["chaptertitle"].get("attribute", None)
        elements = self.__HTMLpraser.getSoup()
        if len(elements) == 1: # must be only one identity
            for element in elements:
                if attribute:
                    chapterTitle = element.get(attribute)
                else:
                    chapterTitle = element.string
        else:
            print("<< Error: More than one title fetched >>")
        return str(chapterTitle)
    
    # works allmost everytime if p tags are used(or other tags within a soup list len(nestedElements) > 1)
    def __nestedContent(self, nestedElements: BeautifulSoup) -> BeautifulSoup:
        flippedElements: list[BeautifulSoup] = []
        for i in range(len(nestedElements) - 1, -1, -1): # remove nesting
            nestedElement: BeautifulSoup = nestedElements[i]
            flippedElements.append(nestedElement) # adds the deepest nested tag
            nestedElement.extract() # remove deepest nested tag -> move to the tag above
        elements: list[BeautifulSoup] = reversed(flippedElements)
        return elements
            
    def getChapterContent(self) -> list[str]: # returns without tags as string
        self.setDefaultTag("p")
        self.fetchChapter("chaptercontent") # fetches the content(<p>) from the chapter
        nestedElements = self.__HTMLpraser.getSoup() # could be nested
        elements: BeautifulSoup = self.nestedChapterContent(nestedElements)
        chapterContent: list[str] = []
        removePattern: str = self.__requestConfig.get("removePattern", None)
        for element in elements:
            if not element.find_all(["script", "div"]) and len(element) != 0: # checks if tag has some content and don't have more tags within
                # appends content if removePattern is None or not within content
                if not removePattern or not removePattern in str(element):
                    chapterContent.append(str(element)) # str -> with tags, .string -> without tags
        return chapterContent