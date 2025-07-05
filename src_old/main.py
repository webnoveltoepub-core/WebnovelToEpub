from PIL import Image
import requests
import time
import json
import os
import io

from Argument import Argument
from ConfigVerify import ConfigVerify
from ConfigHandler import ConfigHandler

from src.Requests.HttpHandler import HttpHandler
from FetchChapterURLs import FetchChapterURLs
from FetchChapterContent import FetchChapterContent
from CreateEPUB import CreateEPUB

import chapterSelection

# sets parameter arguments
param: Argument = Argument()

# checks needed folder
folderConfig: str = "configurations/"
if not os.path.exists(folderConfig):
    print("<< Locale folder named 'configurations/' is needed >>")
    exit()

# verify json configurations via schema
verify = ConfigVerify()
verify.Config()
verify.defaultHttpHeader()
    
# prints out current parameter arguments
param.returnArguments()

# load/set configurations
config = ConfigHandler(param.getUrl())
serverConfig: json = config.getServerConfig()
requestConfig: json = serverConfig["request"] # new mapping
serverHttpHeader: json = config.getServerHttpHeader()

# gets server type (extern = true or intern = false)
typeServer: bool = requestConfig["params"].get("type", True)
if param.getDebug():
    print(f"<< ServerType:{typeServer} -CONFIG- -DEBUGMODE- >>")

# range of sec that will be waited until new request try
timeoutEach: list[float] = param.returnTimeoutEach()
showTime: str = f"*{timeoutEach[0]}*"
if timeoutEach[0] != timeoutEach[1]:
    showTime += f" to *{timeoutEach[1]}*"
print(f"<< Timeout between each request in secounds [{showTime}] >>")
# for websites that need everytime a referer to the page itself
selfReferer: bool = requestConfig.get("selfReferer", False)
# creates request instance
httpRequest = HttpHandler(serverHttpHeader, param.getTimeout(), timeoutEach, selfReferer)

# get chapterURLs
if param.getDebug():
    print(f"<< starting fetching process of chapterlist and it's chapter urls -DEBUGMODE- >>")
fetchURLs = FetchChapterURLs(httpRequest, requestConfig, typeServer, param.getUrl(), param.getDebug(), param.getDebugHtml())
chapterURLs: list[str] = fetchURLs.getChapterURLs()
if param.getDebug():
    print("<< chapterlist fetching process is finished -DEBUGMODE- >>")

# select chapters via external function
selectedChapterURLs: list[str] = chapterSelection.selectChapters(chapterURLs)

if param.getDebug():
    print("<< creating ebook and adding metadata(title, filename, author, cover, ...) -DEBUGMODE- >>")
# sets metadata for ebook file
makeEPUB = CreateEPUB(param.getTitle(), param.getFilename(), param.getAuthor())
# checks if the cover url is set
if param.getCover():
    coverHttpHeader: json = config.getCoverHttpHeader()
    coverSelfReferer: bool = requestConfig.get("coverSelfReferer", False)
    # httpRequest object for cover requests(dedicated server with other config possible)
    httpRequestCover: HttpHandler = HttpHandler(coverHttpHeader, param.getTimeout(), timeoutEach, coverSelfReferer)
    response: requests.Response = None
    while True:
        response: requests.Response = httpRequestCover.makeRequest(param.getCover())
        if isinstance(response, int):
            print(f"<< Cover image [Response: {response}] can't be used >>")
            continue
        break
    # cover is passed to .addCover() as byte steam
    cover: bytes = response.content
    makeEPUB.addCover(cover)
    httpRequestCover.closeSession()

# calculates the time that *could* be the time in total
calcTimeInSec: int = round((timeoutEach[0] + timeoutEach[1]) / 2.0 * len(selectedChapterURLs) + len(selectedChapterURLs) * 0.5)
formatted_time = time.strftime("%H:%M:%S", time.gmtime(calcTimeInSec))
print(f"--- Necessary Time [{formatted_time}] ---")
print("--- Creating ebook ---")
# get content & make book files
chapterCounter: int = 1 # show progess
fetchContent = FetchChapterContent(httpRequest, requestConfig)
for chapterURL in selectedChapterURLs:
    # gets content as plain text (no html format)
    fetchContent.setChapter(chapterURL) # sets response content as chapter
    # returns content converted as plain text/string
    chapterTitle: str = fetchContent.getChapterTitle()
    chapterContent: list[str] = fetchContent.getChapterContent()
    if len(chapterTitle) > 0 and len(chapterContent) > 0: # checks if content is found
        makeEPUB.addChapter(chapterTitle, chapterContent)
        progressInPercent: float = ((chapterCounter / len(selectedChapterURLs)) * 100)
        print("Saving progress: " + str(round(progressInPercent, 1)) + " %")
    else:
        print("<< Error: No content found at current page >>")
    chapterCounter += 1
makeEPUB.writeBook()
print("--- Done ---")