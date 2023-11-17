

#reads source code and strips of whitespace and comments
def cleanLines(filename):
    sourceCode = open(PATH+filename, "r")
    sourceCode = sourceCode.readlines()
    sourceCode = cleanComments(sourceCode)
    splitLines = []
    for line in sourceCode:
        line = line.split(" ")
        splitLines.append(line)
    print(splitLines)
    return sourceCode

#removes the BTW at the end of a line
def cleanComments(lines): 
    #go through each line and strip comments
    cleaned = []
    multiline = 0
    for i in range(0, len(lines)):
        line = re.sub(r' BTW .*$', "", lines[i]).strip()

        if line != '':
            cleaned.append(line)
            #if it starts with OBTW, pop line until you reach TLDR
    return cleaned
