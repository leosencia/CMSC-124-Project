import re
from Variable import Variable

vars = []
class SyntaxAnalyzer:

    def program(self, tokens, lexeme, row):
        i = 0
        
        while(tokens[i] == 'COMMENT'):
            i += 1

        if tokens[i] == 'START':        #encountered start of program
            print("==== PROGRAM START! === \n")
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
        vars.append(Variable(varName, 'NOOB', None))
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
                value, type = searchVarValue(line[i])
                if type != 'YARN':
                    value = typeCasting(value, type, 'YARN', i)
                else:
                    value = value[1:-1]
                string = string + value
            elif tline[i] == 'NUMBR' or tline[i] == 'NUMBAR':
                value = typeCasting(line[i], tline[i], 'YARN', i)
                string = string + value
            elif tline[i] == 'TROOF':
                value = line[i]
                string = string + value
            else:
                raise RuntimeError("Type %r cannot be printed" % (tline[i]))
    print(string)

def searchVarValue(name):
    global vars
    for variable in vars:
        if variable.name == name:
            return variable.value, variable.dataType
    raise RuntimeError('Variable %r does not exist' % (name))

def typeCasting(value, type1, type2, rowNum):
    if type1 == 'NOOB':
        if type2 == 'TROOF':
            return False
        else:
            raise RuntimeError('Encountered error in line %d, cannot typecast NOOB to %r' % (rowNum, type2))
    elif type1 == 'NUMBR' or type1 == 'NUMBAR':
        match type2:
            case 'NUMBAR':
                return float(value)
            case 'NUMBR':
                return int(value)
            case 'YARN':
                return str(value)
            case 'TROOF':
                if value == 0:
                    return 'FAIL'
                else:
                    return 'WIN'
            case _:
                raise RuntimeError('Encountered error in line %d, cannot typecast NUMBR to %r' % (rowNum, type2))
    elif type1 == 'TROOF':
        match type2:
            case 'NUMBAR':
                if value == 'WIN':
                    return 1.0
                else:
                    return 0
            case 'NUMBR':
                if value == 'WIN':
                    return 1
                else:
                    return 0
            case 'YARN':
                return value
            case _:
                raise RuntimeError('Encoutnered error in line %d, cannot typecast TROOF to %r' % (rowNum, type2))
    elif type1 == 'YARN':
        value = value[1:-1]
        match type2:
            case 'NUMBR':
                if bool(re.search(r'-?\d(\d)*', value)):
                    return int(value)
                else:
                    raise RuntimeError('Encountered error in line %d, cannot typecast YARN to %r' % (rowNum, type2))
            case 'NUMBAR':
                if bool(re.search(r'-?\d(\d)*\.\d(\d)*', value)):
                    return float(value)
                else:
                    raise RuntimeError('Encountered error in line %d, cannot typecast YARN to %r' % (rowNum, type2))
            case 'TROOF':
                if value == "":
                    return 'FAIL'
                else:
                    return 'WIN'
            case _:
                 raise RuntimeError('Encountered error in line %d, cannot typecast YARN to %r' % (rowNum, type2))

def printVariables():
    global vars
    for variable in vars:
        print(variable.name)
        print(variable.dataType)
        print(variable.value)
        print("")