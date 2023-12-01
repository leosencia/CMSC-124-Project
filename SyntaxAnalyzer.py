import re

class SyntaxAnalyzer:
    _vars = {}
    
    def program(self, tokens, lexeme, row):
        i = 0
        
        while(tokens[i] == 'COMMENT'):
            i += 1
        if tokens[i] == 'START':        #encountered start of program
            i += 1
            while tokens[i] != 'END' and i < len(tokens):
                if(tokens[i] == 'COMMENT'):
                    i+=1
                    continue
                i = statement(tokens[i], tokens, lexeme, row, i)
            if i == len(tokens):
                raise RuntimeError('End of program not found')   
        else:
            raise RuntimeError('Start of program not found')
        
def statement(token, tokens, lexeme, row, i):
    tline = []
    line = []
    rowNum = row[i]
    # print(rowNum)
    while rowNum == row[i]:
        tline.append(tokens[i])
        line.append(lexeme[i])
        i += 1
    
    if tline[0] == 'PRINT':
        printLine(line, tline)
    return i

def printLine(line, tline):
    #assume muna na YARN lang ung priniprint

    string = ""
    for i in range(0, len(line)):
        if tline[i] != 'PRINT' and tline[i] != 'COMMENT':
            if tline[i] == 'YARN':
                string = string + line[i][1:-1]
    
    print(string)
