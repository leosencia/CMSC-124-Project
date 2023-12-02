import re
from Variable import Variable

vars = []
class SyntaxAnalyzer:

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

                if tokens[i] == 'WAZZUP':
                    i += 1
                    i = isVarDec(tokens, lexeme, row, i)
                

                i = statement(tokens, lexeme, row, i)
                
                if i >= len(tokens):
                    break
            if i == len(tokens):
                raise RuntimeError('End of program not found')
            # printVariables()
        else:
            raise RuntimeError('Start of program not found')
def isVarDec(tokens, lexeme, row, i):
    maxlen = len(tokens)
    while(tokens[i] != 'BUHBYE'):
        if tokens[i] == 'COMMENT': #aka BTW (single line comment)
            #comments are stored all in one, if it's a multiline is when we iterate thru so this is fine
            i += 1
            continue
        elif tokens[i] == 'VAR_DEC':
            #build line
            rowNum = row[i]
            line = []
            tline = []
            while rowNum == row[i]:
                line.append(lexeme[i])
                tline.append(tokens[i])
                i += 1
            storeVariable(tline, line, rowNum)
        else:
            raise RuntimeError('Unexpected %r on line %d, Only variable declarations are allowed in this section' % (lexeme[i], row[i]))

        if i >= maxlen:
            raise RuntimeError('Encountered end of file')
    return i

def storeVariable(tline, line, rowNum):
    global vars

    i = 1
    maxlength = len(tline)
    if tline[i] == 'VARIABLE':
        varName = line[i][:-1]
        i += 1
    else:
        raise RuntimeError('Expected VARIABLE NAME on line %d' % (rowNum))

    if i >= maxlength:
        type = None
        value = None
        vars.append(Variable(varName, type, value))
        return

    if tline[i] == 'ITZ':
        i += 1
    else:
        raise RuntimeError('Expected \'ITZ\' on line %d' % (rowNum))
    
    if i >= maxlength:
        raise RuntimeError('Encountered end of file!')
    
    if tline[i] == 'NOOB' or tline[i] == 'YARN' or tline[i] == 'TROOF' or tline[i] == 'NUMBAR' or tline[i] == 'NUMBR' or tline[i] == 'VARIABLE':
        type = tline[i]
        value = line[i]
        vars.append(Variable(varName, type, value))
        return
    else:
        raise RuntimeError('Variable declaration can only be to a YARN, TROOF, NOOB etch')

def statement(tokens, lexeme, row, i):
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
    elif tline[0] == 'VAR_DEC':
        raise RuntimeError("Unexpected variable declaration at line %d" % (rowNum))
    return i

def printLine(line, tline):
    #assume muna na YARN lang ung priniprint

    string = ""
    for i in range(0, len(line)):
        if tline[i] != 'PRINT' and tline[i] != 'COMMENT':
            if tline[i] == 'YARN':
                string = string + line[i][1:-1]
            elif tline[i] == 'VARIABLE':
                string = string + searchVarValue(line[i])
    print(string)

def searchVarValue(name):
    global vars
    for variable in vars:

        if variable.name == name:
            return variable.value
    raise RuntimeError('Variable %r does not exist' % (name))

def printVariables():
    global vars
    for variable in vars:
        print(variable.name)
        print(variable.dataType)
        print(variable.value)
        print("")