def createWordLib():
    with open("/usr/share/dict/words") as allWords:
        for line in allWords:
            lines = line.replace("'s",'').strip('\n')
            
            if len(lines) >= 7:
                with open('files/sourceWords.txt', 'a') as wordLog:
                    print(lines, file = wordLog)
            if len(lines) >=3:
                with open('files/guessWords.txt','a') as guessLog:
                    print(lines, file = guessLog)
