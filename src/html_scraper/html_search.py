from bs4 import BeautifulSoup

# simplyfies the filtering process as layers with bs4 searchElements(searchSection) as an example
class HTMLSearch:     
    # for soup changing after object creation
    def setSoup(self, soup: BeautifulSoup) -> None:
        self.__soup = soup
    def getSoup(self) -> BeautifulSoup:
        return self.__soup
    
    # returns content of soup as formated text/string (via prettify())
    def returnSoup(self):
        if not self.__soup:
            print("<< B4SError: Soup is empty >>")
        elif isinstance(self.__soup, list):
            for element in self.__soup:
                print(element.prettify())
        else:
            print(self.__soup.prettify())
        
    # searches for a group of elements by the given parameters and creates a soup list
    # searchElements could be based on the pre filtering by searchSection 'cause find_all can be based on a return of .find()
    def searchElements(self, tagHtml: str = None, classHtml: str = None, idHtml: str = None) -> None: # filters tag, class and id within the same element
        localSoup: BeautifulSoup = self.__soup
        # tags are required
        if classHtml or idHtml:
            if classHtml and idHtml:
                elementsSoup = localSoup.find_all(tagHtml, class_=classHtml, idHtml=idHtml)
            else:
                if classHtml:
                    elementsSoup = localSoup.find_all(tagHtml, class_=classHtml)
                elif idHtml:
                    elementsSoup = localSoup.find_all(tagHtml, id=idHtml)
        else:
            elementsSoup = localSoup.find_all(tagHtml)
        self.setSoup(elementsSoup)
            
    # searches for the first elements(and it's under elements) that fits with the given parameters
    def searchSection(self, classHtml: str = None, idHtml: str = None) -> None: # filters class and id within the same element
        localSoup: BeautifulSoup = self.__soup
        if classHtml and idHtml:
            sectionSoup = localSoup.find(class_=classHtml, id=idHtml)
        else:
            if classHtml:
                sectionSoup = localSoup.find(class_=classHtml)
            elif idHtml:
                sectionSoup = localSoup.find(id=idHtml)
        self.setSoup(sectionSoup)