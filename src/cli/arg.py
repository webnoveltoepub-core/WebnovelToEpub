import argparse

# for parameter arguments and general program controlling
class Argument:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog = "WebnovelToEpub - website scraper fetching & converting webnovels into ebooks",
            description = """
                WebnovelToEpub is a Python based application that targets simple webnovel sites.  
                It's fully configurable and targets simple webnovel sites with the purpose to create configs  
                for the wished websites even if those sites are new or unknown.
            """,
            epilog = "Configuration guide: https://github.com/TheUnixDemon/WebnovelToEpub/blob/main/CONFIG.md")
        
        parser.add_argument("-u", "--url", help = "url of chosen webnovel page *required*", required = True)
        parser.add_argument("-t", "--title", help = "book title *required*", required = True)
        parser.add_argument("-a", "--author", help = "name of author", default = "Unknown")
        parser.add_argument("-c", "--cover", help = "cover for the ebook")
        parser.add_argument("-f", "--filename", help = "custom filename")
        parser.add_argument("-T", "--timeout", help = "sets request connection time limit *default 15sec*", type = int, default = 15)
        parser.add_argument("-l", "--latency", type = float, help = "adds latency to the requests in between", default = 0.0)
        parser.add_argument("-hl", "--humanlike", action = "store_false", help = "waits 5-10sec between requests *default*", default = True)
        parser.add_argument("-Hl", "--morehumanlike", action = "store_true", help = "waits 15-30sec between requests", default = False)
        parser.add_argument("-d", "--debug", action = "store_true", help = "enable debug output", default = False)
        parser.add_argument("-D", "--debughtml", action = "store_true", help = "enable debug output with html", default = False)
        self.__args: argparse = parser.parse_args()

        # ensures correct values
        self.__args.filename = (self.__args.filename if self.__args.filename else self.__args.title) + ".epub"
        self.__args.humanlike = (False if self.__args.morehumanlike else self.__args.humanlike)
        self.__args.debug = (False if self.__args.debughtml else self.__args.debug)

    def getUrl(self) -> str:
        return self.__args.url
    def getTitle(self) -> str:
        return self.__args.title
    def getAuthor(self) -> str:
        return self.__args.author
    def getCover(self) -> str:
        return self.__args.cover
    def getFilename(self):
        return self.__args.filename
    def getTimeout(self) -> int:
        return self.__args.timeout
    def getLatency(self) -> float:
        # if the passed float was negative
        return abs(self.__args.latency)
    def getHumanlike(self) -> bool:
        return self.__args.humanlike
    def getMorehumanlike(self) -> bool:
        return self.__args.morehumanlike
    def getDebug(self) -> bool:
        return self.__args.debug
    def getDebugHtml(self) -> bool:
        return self.__args.debughtml
    
    # returns a output for the user
    def returnArguments(self):
        print(f"url:{self.getUrl()}, "
              f"title:{self.getTitle()}, "
              f"author:{self.getAuthor()}, "
              f"cover:{self.getCover()}, "
              f"filename:{self.getFilename()}, " 
              f"timeout:{self.getTimeout()}, "
              f"latency:{self.getLatency()}, "
              f"humanlike:{self.getHumanlike()}, "
              f"morehumanlike:{self.getMorehumanlike()}, "
              f"debugmode:{self.getDebug()}")

    # returns time to wait if connection time limit is reached
    # source of the values are humanlike, morehumanlike and latency
    def returnTimeoutEach(self) -> list[float]:
        timeoutEach: list[float] = [0.0, 0.0]
        if self.getMorehumanlike():
            timeoutEach[0] = 15.0; timeoutEach[1] = 30.0
        elif self.getHumanlike():
            timeoutEach[0] = 5.0; timeoutEach[1] = 15.0
        timeoutEach[0] += self.getLatency(); timeoutEach[1] += self.getLatency()
        return timeoutEach

