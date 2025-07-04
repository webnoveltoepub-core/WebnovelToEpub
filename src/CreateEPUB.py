from ebooklib import epub
from io import BytesIO
from PIL import Image

# writes the epub file
class CreateEPUB:
    def __init__(self, bookTitle: str, bookFilename: str, bookAuthor: str):
        # part of book structure
        self.__ebook = epub.EpubBook()
        self.__ebook.spine = ["nav"]
        self.__ebook.toc = []
        # metadata
        self.__bookTitle = bookTitle
        self.__bookAuthor = bookAuthor
        self.__bookLanguage = "en"
        self.__bookFilename = bookFilename
        self.__xhtmlFileNumber: int = 1 # for valid file names
        self.addMetadata() # adds metadata to the book
            
    def addMetadata(self) -> None:
        self.__ebook.set_title(self.__bookTitle)
        self.__ebook.set_language(self.__bookLanguage)
        self.__ebook.add_author(self.__bookAuthor)     

    # converts cover into png and saves it as ebook cover
    def addCover(self, coverImage: bytes) -> None:
        # convert image into png
        cover: Image = Image.open(BytesIO(coverImage))
        img_bytes: BytesIO = BytesIO()
        cover.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        # saves coverted cover in class attribute
        self.__ebook.set_cover("cover.png", img_bytes.getvalue(), True)
        
    # sets filename for current chapter
    def addChapter(self, chapterTitle: str, chapterContent: list[str]) -> None:
        xhtmlFilename: str = f"file{self.__xhtmlFileNumber}.xhtml" # intern chapter file
        self.__xhtmlFileNumber += 1
        # adds new chapter
        currentChapter: epub = epub.EpubHtml( # adds metadata for current chapter
            title = chapterTitle,
            file_name = xhtmlFilename,
            lang = self.__bookLanguage
            )
        # adds chaptercontent to chapterfile, puts into the ebook file and sets an entry into the pine, 
        titleHTML = f"<h1 id='chapter'>{chapterTitle}</h1>"
        contentHTML = "\n".join(chapterContent) # para1\npara2\npara3; to not make a single paragraph with every content
        currentChapter.set_content(titleHTML + "\n" + contentHTML) # sets content into chapterfile
        self.__ebook.add_item(currentChapter) # adds current chapter to book
        # toc&spine sets the structure and index within the book
        self.__ebook.toc.append(epub.Link(xhtmlFilename, chapterTitle, "chapter"))
        self.__ebook.spine.append(currentChapter)

    def writeBook(self) -> None:
        self.__ebook.add_item(epub.EpubNcx())
        self.__ebook.add_item(epub.EpubNav())
        epub.write_epub(self.__bookFilename, self.__ebook)