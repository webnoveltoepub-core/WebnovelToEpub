# gets all chapters and return choosen chapters as list
def selectChapters(chapterURLs: list[str]) -> list[str]:
    firstChapter: int = 1
    lastChapter: int = len(chapterURLs)

    print("--- Found chapters ---")
    # prints out other chapter layout if len(chapterURLs) > 300
    if len(chapterURLs) > 300:
        lastNumber = str(len(chapterURLs)) + ": "
        print(f"{firstChapter}:{chapterURLs[0]} ... {lastChapter}:{chapterURLs[-1]}") #  [-1] equals to (len(chapterURLs) - 1)
    else:
        chapterNumber: int = 1 # counter for chapters
        for chapterURL in chapterURLs:
            print(f"{chapterNumber}: {chapterURL}")
            chapterNumber += 1
            
    while True:
        print("--- Chapter selection ---")
        while True:
            try:        
                chapterStart: str = input("Enter first chapter: ")
                chapterEnd: str = input("Enter last chapter: ")
                
                # checks if something is entered
                if not chapterStart or not chapterEnd: # convert str into int
                    raise Exception("Input cannot be empty")
                
                # checks if a number is entered
                chapterStart = int(chapterStart)
                chapterEnd = int(chapterEnd)
                    
                # checks if numbers are in range
                rangeError: str = f"Entered chapter numbers has to be in range of {firstChapter} and {lastChapter}"
                if chapterStart < firstChapter or chapterStart > lastChapter:
                    raise Exception(rangeError)
                if chapterEnd < firstChapter or chapterEnd > lastChapter:
                    raise Exception(rangeError)
                
                if chapterStart > chapterEnd:
                    raise Exception("Entered first chapter has to be smaller or equal to the last entered chapter.")
            except ValueError:
                print("Error: Input has to be a number")
            except Exception as e:
                print(f"Error:{e}")
            else: # no errors happened
                break

        # confirm choosen chapters
        print("--- selected chapters ---")
        print(f"{firstChapter}:{chapterURLs[chapterStart - 1]} ... {len(chapterURLs[chapterStart - 1:chapterEnd])}: {chapterURLs[chapterEnd - 1]}")
        while True:
            try:
                answer: str = input("Are those the selected chapters that you want? (y/n): ").lower()
                if answer not in ["y", "n"]:
                    raise ValueError("Non valid answer. Please enter only 'n' or 'y'")
                elif answer == "y":
                    selectedChapterURLs: list[str] = chapterURLs[chapterStart - 1:chapterEnd]
                    return selectedChapterURLs
                # repeats choice to choose chapter that are to be saved
                else:
                    break
            # repeat answer input
            except ValueError as e:
                print(f"Error:{e}") 