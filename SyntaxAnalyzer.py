import re
from Variable import Variable
from collections import deque

vars = [Variable("IT", "NOOB", "")]
returnVals = []
runtimeError = False


class SyntaxAnalyzer:
    def program(self, tokens, lexeme, row):
        global returnVals, runtimeError
        # reset variables
        returnVals = []
        runtimeError = False
        i = 0

        while tokens[i] == "COMMENT":
            i += 1

        if tokens[i] == "START":  # encountered start of program
            print("==== PROGRAM START! === \n")
            i += 1
            while tokens[i] != "END" and i < len(tokens):
                if tokens[i] == "COMMENT":
                    i += 1
                    continue

                if tokens[i] == "WAZZUP":
                    i += 1
                    i = isVarDec(tokens, lexeme, row, i)

                i = statement(tokens, lexeme, row, i)

                if i >= len(tokens):
                    break
            if i == len(tokens):
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("End of program not found")
                return returnVals
                raise RuntimeError("End of program not found")
            # printVariables()
        else:
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append("Start of program not found")
            return returnVals
            raise RuntimeError("Start of program not found")
        return returnVals


def isVarDec(tokens, lexeme, row, i):
    global vars, returnVals, runtimeError
    maxlen = len(tokens)
    while tokens[i] != "BUHBYE":
        if tokens[i] == "COMMENT":  # aka BTW (single line comment)
            # comments are stored all in one, if it's a multiline is when we iterate thru so this is fine
            i += 1
            continue
        elif tokens[i] == "VAR_DEC":
            # build line
            rowNum = row[i]
            line = []
            tline = []
            while rowNum == row[i]:
                line.append(lexeme[i])
                tline.append(tokens[i])
                i += 1
            storeVariable(tline, line, rowNum)
        else:
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append(
                "Unexpected "
                + str(lexeme[i])
                + " on line "
                + str(row[i])
                + ". Only variable declarations are allowed in this section"
            )
            return returnVals
            raise RuntimeError(
                "Unexpected %r on line %d, Only variable declarations are allowed in this section"
                % (lexeme[i], row[i])
            )

        if i >= maxlen:
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append("Expected end of file")
            return returnVals
            raise RuntimeError("Encountered end of file")
    return i


def storeVariable(tline, line, rowNum):
    global vars, returnVals, runtimeError
    i = 1
    maxlength = len(tline)
    if tline[i] == "VARIABLE":
        varName = line[i].strip()
        i += 1
    else:
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append("Expected VARIABLE NAME on line " + str(rowNum))
        return returnVals
        raise RuntimeError("Expected VARIABLE NAME on line %d" % (rowNum))

    if i >= maxlength:
        vars.append(Variable(varName, "NOOB", None))
        return

    if tline[i] == "ITZ":
        i += 1
    else:
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append("Expected 'ITZ' on line " + str(rowNum))
        return returnVals
        raise RuntimeError("Expected 'ITZ' on line %d" % (rowNum))

    if i >= maxlength:
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append("Variable must have a value!")
        return returnVals
        raise RuntimeError("Variable must have a value!")

    if (
        tline[i] == "NOOB"
        or tline[i] == "YARN"
        or tline[i] == "TROOF"
        or tline[i] == "NUMBAR"
        or tline[i] == "NUMBR"
        or tline[i] == "VARIABLE"
    ):
        type = tline[i]
        value = line[i]
        vars.append(Variable(varName, type, value))
        return
    else:
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append("Variable declaration can only be to a YARN, TROOF, NOOB etc")
        return returnVals
        raise RuntimeError(
            "Variable declaration can only be to a YARN, TROOF, NOOB etc"
        )


def statement(tokens, lexeme, row, i):
    global vars, returnVals, runtimeError
    tline = []
    line = []
    rowNum = row[i]
    # print(rowNum)
    while rowNum == row[i]:
        tline.append(tokens[i])
        line.append(lexeme[i])
        i += 1

    if tline[0] == "PRINT":
        printLine(line, tline, i)
    elif tline[0] == "VAR_DEC":
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append("Unexpected variable declaration at line " + str(rowNum))
        return returnVals
        raise RuntimeError("Unexpected variable declaration at line %d" % (rowNum))
    elif tline[0] == "BOOL_OPER":
        value = boolOpRegion(line, tline, 0, rowNum)
        storeVariables("IT", "TROOF", value)
        # print(boolOpRegion(line, tline, 0, rowNum))
    elif tline[0] == "COMPARISON":
        storeVariables("IT", "TROOF", comparison(line, tline, 0, rowNum))
        # print(comparison(line, tline, 0, rowNum))
    elif tline[0] == "MATH":
        value = mathOp(line, tline, 0, rowNum)
        if isinstance(value, int):
            storeVariables("IT", "NUMBR", value)
        else:
            storeVariables("IT", "NUMBAR", value)
    elif tline[0] == "INPUT":
        getInput(line, tline, 0, rowNum)
    return i


def getInput(line, tline, i, rowNum):
    global returnVals, runtimeError
    i += 1
    if tline[i] == "VARIABLE":
        varName = line[i]
        inputSTR = input("")
        storeVariables(varName, "YARN", inputSTR)
    else:
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append(
            "Error in line "
            + str(rowNum)
            + ", expected VARIABLE instead of "
            + str(line[i])
        )
        return returnVals
        raise RuntimeError(
            "Error in line %d, expected VARIABLE instead of %r" % (rowNum, line[i])
        )


def comparison(line, tline, i, rowNum):
    global returnVals, runtimeError
    compQ = []
    # print(line)
    if line[i] == "BOTH SAEM":
        i += 1
        if tline[i] == "NUMBR" or tline[i] == "NUMBAR":
            compQ.append([tline[i], line[i]])
            i += 1
        elif tline[i] == "VARIABLE":
            value, type = searchVarValue(line[i])
            compQ.append([type, value])
            i += 1
        else:
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append(
                "Expected NUMBR, NUMBAR, or VARIABLE at line " + str(rowNum)
            )
            return returnVals
            raise RuntimeError(
                "Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum)
            )
        if tline[i] != "AN":
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append("Expected AN at line " + str(rowNum))
            return returnVals
            raise RuntimeError("Expected AN at line %d" % (rowNum))
        i += 1
        if line[i] == "BIGGR OF" or line[i] == "SMALLR OF":
            compQ.append(line[i])
            i += 1
            if tline[i] == "NUMBR" or tline[i] == "NUMBAR":
                compQ.append([tline[i], line[i]])
                i += 1
            elif tline[i] == "VARIABLE":
                value, type = searchVarValue(line[i])
                compQ.append([type, value])
                i += 1
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Expected NUMBR, NUMBAR, or VARIABLE at line" + str(rowNum)
                )
                return returnVals
                raise RuntimeError(
                    "Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum)
                )
            if compQ[0][1] != compQ[2][1]:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Value mismatch - operand 1 and 2 ("
                    + str(compQ[0][1])
                    + " and "
                    + str(compQ[2][1])
                    + ") must be same"
                )
                return returnVals
                raise RuntimeError(
                    "Value mismatch - operand 1 and 2 (%r and %r) must be same"
                    % (compQ[0][1], compQ[2][1])
                )
            if tline[i] != "AN":
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("Expected AN at line " + str(rowNum))
                return returnVals
                raise RuntimeError("Expected AN at line %d" % (rowNum))
            i += 1
            if tline[i] == "NUMBR" or tline[i] == "NUMBAR":
                compQ.append([tline[i], line[i]])
                i += 1
            elif tline[i] == "VARIABLE":
                value, type = searchVarValue(line[i])
                compQ.append([type, value])
                i += 1
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Expected NUMBR, NUMBAR, VARIABLE at line" + str(rowNum)
                )
                return returnVals
                raise RuntimeError(
                    "Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum)
                )
        elif tline[i] == "NUMBR" or tline[i] == "NUMBAR":
            compQ.append([tline[i], line[i]])
            i += 1
        elif tline[i] == "VARIABLE":
            value, type = searchVarValue(line[i])
            compQ.append([type, value])
            i += 1
        else:
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append(
                "Expected NUMBR, NUMBAR, VARIABLE, BIGGR OF, or SMALLR OF at line"
                + str(rowNum)
            )
            return returnVals
            raise RuntimeError(
                "Expected NUMBR, NUMBAR, VARIABLE, BIGGR OF, or SMALLR OF at line %d"
                % (rowNum)
            )

        # print(compQ)
        if compQ[1] == "BIGGR OF":
            if compQ[2][0] != compQ[3][0]:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Type mismatch - cannot compare "
                    + str(compQ[0][0])
                    + " and "
                    + str(compQ[1][0])
                )
                return returnVals
                raise RuntimeError(
                    "Type mismatch - cannot compare %r and %r"
                    % (compQ[0][0], compQ[1][0])
                )
            if compQ[2][0] == "NUMBR":
                if int(compQ[2][1]) >= int(compQ[3][1]):
                    return "WIN"
                else:
                    return "FAIL"
            elif compQ[2][0] == "NUMBAR":
                if float(compQ[2][1]) >= float(compQ[3][1]):
                    return "WIN"
                else:
                    return "FAIL"
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("Unexpected type " + str(compQ[2][0]))
                return returnVals
                raise RuntimeError("Unexpected type %r" % (compQ[2][0]))
        elif compQ[1] == "SMALLR OF":
            if compQ[2][0] != compQ[3][0]:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Type mismatch - cannot compare "
                    + str(compQ[0][0])
                    + " and "
                    + str(compQ[1][0])
                )
                return returnVals
                raise RuntimeError(
                    "Type mismatch - cannot compare %r and %r"
                    % (compQ[0][0], compQ[1][0])
                )
            if compQ[2][0] == "NUMBR":
                if int(compQ[2][1]) <= int(compQ[3][1]):
                    return "WIN"
                else:
                    return "FAIL"
            elif compQ[2][0] == "NUMBAR":
                if float(compQ[2][1]) <= float(compQ[3][1]):
                    return "WIN"
                else:
                    return "FAIL"
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("Unexpected type " + str(compQ[2][0]))
                return returnVals
                raise RuntimeError("Unexpected type %r" % (compQ[2][0]))
        else:
            if compQ[0][0] != compQ[1][0]:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Type mismatch - cannot compare "
                    + str(compQ[0][0])
                    + " and "
                    + str(compQ[1][0])
                )
                return returnVals
                raise RuntimeError(
                    "Type mismatch - cannot compare %r and %r"
                    % (compQ[0][0], compQ[1][0])
                )
            if compQ[0][1] == compQ[1][1]:
                return "WIN"
            else:
                return "FAIL"
    elif line[i] == "DIFFRINT":
        i += 1
        if tline[i] == "NUMBR" or tline[i] == "NUMBAR":
            compQ.append([tline[i], line[i]])
            i += 1
        elif tline[i] == "VARIABLE":
            value, type = searchVarValue(line[i])
            compQ.append([type, value])
            i += 1
        else:
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append(
                "Expected NUMBR, NUMBAR, or VARIABLE at line " + str(rowNum)
            )
            return returnVals
            raise RuntimeError(
                "Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum)
            )
        if tline[i] != "AN":
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append("Expected AN at line " + str(rowNum))
            return returnVals
            raise RuntimeError("Expected AN at line %d" % (rowNum))
        i += 1
        if line[i] == "BIGGR OF" or line[i] == "SMALLR OF":
            compQ.append(line[i])
            i += 1
            if tline[i] == "NUMBR" or tline[i] == "NUMBAR":
                compQ.append([tline[i], line[i]])
                i += 1
            elif tline[i] == "VARIABLE":
                value, type = searchVarValue(line[i])
                compQ.append([type, value])
                i += 1
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Expected NUMBR, NUMBAR, or VARIABLE at line " + str(rowNum)
                )
                return returnVals
                raise RuntimeError(
                    "Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum)
                )
            if compQ[0][1] != compQ[2][1]:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Value mismatch on line "
                    + str(rowNum)
                    + "("
                    + str(compQ[0][1])
                    + " and "
                    + str(compQ[2][1])
                    + ") must be same"
                )
                return returnVals
                raise RuntimeError(
                    "Value mismatch on line %d (%r and %r) must be same"
                    % (rowNum, compQ[0][1], compQ[2][1])
                )
            if tline[i] != "AN":
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("Expected AN at line" + str(rowNum))
                return returnVals
                raise RuntimeError("Expected AN at line %d" % (rowNum))
            i += 1
            if tline[i] == "NUMBR" or tline[i] == "NUMBAR":
                compQ.append([tline[i], line[i]])
                i += 1
            elif tline[i] == "VARIABLE":
                value, type = searchVarValue(line[i])
                compQ.append([type, value])
                i += 1
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Expected NUMBR, NUMBAR, or VARIABLE at line " + str(rowNum)
                )
                return returnVals
                raise RuntimeError(
                    "Expected NUMBR, NUMBAR, or VARIABLE at line %d" % (rowNum)
                )
        elif tline[i] == "NUMBR" or tline[i] == "NUMBAR":
            compQ.append([tline[i], line[i]])
            i += 1
        elif tline[i] == "VARIABLE":
            value, type = searchVarValue(line[i])
            compQ.append([type, value])
            i += 1
        else:
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append(
                "Expected NUMBR, NUMBAR, or VARIABLE at line " + str(rowNum)
            )
            return returnVals
            raise RuntimeError(
                "Expected NUMBR, NUMBAR, VARIABLE, BIGGR OF, or SMALLR OF at line %d"
                % (rowNum)
            )

        # print(compQ)
        if compQ[1] == "BIGGR OF":
            if compQ[2][0] != compQ[3][0]:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Type mismatch - cannot compare "
                    + str(compQ[0][0])
                    + " and "
                    + str(compQ[1][0])
                )
                return returnVals
                raise RuntimeError(
                    "Type mismatch - cannot compare %r and %r"
                    % (compQ[0][0], compQ[1][0])
                )
            if compQ[2][0] == "NUMBR":
                if int(compQ[3][1]) >= int(compQ[2][1]):
                    return "WIN"
                else:
                    return "FAIL"
            elif compQ[2][0] == "NUMBAR":
                if float(compQ[3][1]) >= float(compQ[2][1]):
                    return "WIN"
                else:
                    return "FAIL"
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("Unexpected type " + str(compQ[2][0]))
                return returnVals
                raise RuntimeError("Unexpected type %r" % (compQ[2][0]))
        elif compQ[1] == "SMALLR OF":
            if compQ[2][0] != compQ[3][0]:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Type mismatch - cannot compare "
                    + str(compQ[0][0])
                    + " and "
                    + str(compQ[1][0])
                )
                return returnVals
                raise RuntimeError(
                    "Type mismatch - cannot compare %r and %r"
                    % (compQ[0][0], compQ[1][0])
                )
            if compQ[2][0] == "NUMBR":
                if int(compQ[3][1]) <= int(compQ[2][1]):
                    return "WIN"
                else:
                    return "FAIL"
            elif compQ[2][0] == "NUMBAR":
                if float(compQ[3][1]) <= float(compQ[2][1]):
                    return "WIN"
                else:
                    return "FAIL"
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("Unexpected type " + str(compQ[2][0]))
                return returnVals
                raise RuntimeError("Unexpected type %r" % (compQ[2][0]))
        else:
            if compQ[0][0] != compQ[1][0]:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Type mismatch - cannot compare "
                    + str(compQ[0][0])
                    + " and "
                    + str(compQ[1][0])
                )
                return returnVals
                raise RuntimeError(
                    "Type mismatch - cannot compare %r and %r"
                    % (compQ[0][0], compQ[1][0])
                )
            if compQ[0][1] != compQ[1][1]:
                return "WIN"
            else:
                return "FAIL"


# function for parsing prefix notation math operations
def parse(tokens):
    global returnVals, runtimeError
    if not tokens:
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append("Unexpected end of statement.")
        return returnVals
        raise RuntimeError("Unexpected end of statement.")
    else:
        token = tokens.popleft()
        if token == "+":
            return parse(tokens) + parse(tokens)
        elif token == "-":
            return parse(tokens) - parse(tokens)
        elif token == "/":
            return parse(tokens) / parse(tokens)
        elif token == "*":
            return parse(tokens) * parse(tokens)
        elif token == "%":
            return parse(tokens) % parse(tokens)
        elif token == "max":
            return max(parse(tokens), parse(tokens))
        elif token == "min":
            return min(parse(tokens), parse(tokens))
        else:
            return token


def mathOp(line, tline, i, rowNum):
    global returnVals, runtimeError
    op = []
    num_of_operations = 0
    num_of_AN = 0

    while i < len(line):
        if line[i] == "SUM OF":
            op.append("+")
            i += 1
            num_of_operations += 1
        elif line[i] == "DIFF OF":
            op.append("-")
            i += 1
            num_of_operations += 1
        elif line[i] == "PRODUKT OF":
            op.append("*")
            i += 1
            num_of_operations += 1
        elif line[i] == "QUOSHUNT OF":
            op.append("/")
            i += 1
            num_of_operations += 1
        elif line[i] == "MOD OF":
            op.append("%")
            i += 1
            num_of_operations += 1
        elif line[i] == "BIGGR OF":
            op.append("max")
            i += 1
            num_of_operations += 1
        elif line[i] == "SMALLR OF":
            op.append("min")
            i += 1
            num_of_operations += 1
        else:
            if tline[i] == "NUMBR":
                op.append(int(line[i]))
                i += 1
            elif tline[i] == "NUMBAR":
                op.append(float(line[i]))
                i += 1
            elif tline[i] == "VARIABLE":
                value, _ = searchVarValue(line[i])
                op.append(value)
                i += 1
            elif tline[i] == "YARN":
                value = typeCasting(line[i], tline[i], "NUMBAR", rowNum)
                op.append(value)
                i += 1
            elif tline[i] == "AN":
                i += 1
                num_of_AN += 1
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Unexpected " + str(line[i]) + " at line " + str(rowNum)
                )
                return returnVals
                raise RuntimeError("Unexpected %r at line %d" % (line[i], rowNum))
            i += 1

    expected_operands = num_of_operations + 1
    actual_operands = len(op) - (num_of_AN + num_of_operations)
    if expected_operands != actual_operands:
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append(
            "Expected "
            + str(expected_operands)
            + " operands, but found "
            + str(actual_operands)
            + " at line "
            + str(rowNum)
        )
        return returnVals
        raise RuntimeError(
            "Expected %d operands, but found %d at line %d"
            % (expected_operands, actual_operands, rowNum)
        )
    else:
        return parse(deque(op))


def boolOp(line, tline, i, rowNum):
    global returnVals, runtimeError
    if tline[i] == "BOOL_OPER":
        opAddress = i
        boolQ = []
        i += 1
        i, boolQ0 = boolOp(line, tline, i, rowNum)
        boolQ.append(boolQ0)
        if line[opAddress] == "NOT":
            if boolQ[0] == "WIN":
                return i, "FAIL"
            else:
                return i, "WIN"
        i += 1
        if tline[i] != "AN":
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append("Expected AN at line " + str(rowNum))
            return returnVals
            raise RuntimeError("Expected AN at line %d" % (rowNum))
        i += 1
        i, boolQ1 = boolOp(line, tline, i, rowNum)
        boolQ.append(boolQ1)
        # print(boolQ)
        if line[opAddress] == "BOTH OF":
            if boolQ[0] == "WIN" and boolQ[1] == "WIN":
                return i, "WIN"
            else:
                return i, "FAIL"
        elif line[opAddress] == "EITHER OF":
            if boolQ[0] == "WIN" or boolQ[1] == "WIN":
                return i, "WIN"
            else:
                return i, "FAIL"
        elif line[opAddress] == "WON OF":
            if boolQ[0] != boolQ[1] and (boolQ[0] == "WIN" or boolQ[1] == "WIN"):
                return i, "WIN"
            else:
                return i, "FAIL"
    elif tline[i] == "VARIABLE":
        if i < len(line) - 1:
            line[i] = line[i].strip()
        value, type = searchVarValue(line[i])
        if type != "TROOF":
            value = typeCasting(value, type, "TROOF", rowNum)
        return i, value
    elif tline[i] == "TROOF":
        return i, line[i]
    else:
        runtimeError = True
        returnVals.append(runtimeError)
        returnVals.append("Unexpected " + str(line[i]) + " at line " + str(rowNum))
        return returnVals
        raise RuntimeError("Unexpected %r at line %d, %d" % (line[i], rowNum))


def boolOpRegion(line, tline, i, rowNum):
    global returnVals, runtimeError
    if line[i] == "ALL OF" or line[i] == "ANY OF":
        if line[i] == "ALL OF":
            initCond = "WIN"
            terminateCond = "WIN"
        elif line[i] == "ANY OF":
            terminateCond = "FAIL"
            initCond = "FAIL"
        i += 1
        while i < len(line):
            if initCond == terminateCond:
                i, initCond = boolOp(line, tline, i, rowNum)
                i += 1
            if line[i] == "AN":
                i += 1
            elif (
                tline[i] == "BOOL_OPER" or tline[i] == "TROOF" or tline[i] == "VARIABLE"
            ):
                i += 1
            elif line[i] == "MKAY":
                break
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("Type " + str(tline[i]) + " cannot be printed")
                return returnVals
                raise RuntimeError(
                    "Expected AN at line %d, %d but encountered %r"
                    % (rowNum, i, line[i])
                )
        if i != len(line) and tline[i] != "COMMENT":
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append(
                "Error: Unexpected ", str(line[i + 1]), " in line ", str(rowNum)
            )
            return returnVals
            raise RuntimeError("Unexpected %r in line %d" % (line[i + 1], rowNum))
        # print("i: "+str(i))
        return initCond
    else:
        j, k = boolOp(line, tline, i, rowNum)
        if j != len(line) - 1 and tline[j + 1] != "COMMENT":
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append(
                "Error: Unexpected ", str(line[j + 1]), " in line ", str(rowNum)
            )
            return returnVals
            raise RuntimeError("Unexpected %r in line %d" % (line[j + 1], rowNum))
        else:
            return k


def printLine(line, tline, rowNum):
    global returnVals, runtimeError
    # assume muna na YARN lang ung priniprint
    string = ""
    for i in range(0, len(line)):
        if tline[i] != "PRINT" and tline[i] != "COMMENT":
            if tline[i] == "YARN":
                string = string + line[i].replace('"', "")
            elif tline[i] == "VARIABLE":
                value, type = searchVarValue(line[i])
                if type != "YARN":
                    value = typeCasting(value, type, "YARN", i)
                else:
                    value = value.strip()
                # print(value)
                string = string + value
            elif tline[i] == "NUMBR" or tline[i] == "NUMBAR":
                value = typeCasting(line[i], tline[i], "YARN", i)
                string = string + value
            elif tline[i] == "TROOF":
                value = line[i]
                string = string + value
            elif tline[i] == "BOOL_OPER":
                value = boolOpRegion(line, tline, i, rowNum)
                string = string + value
                break
            elif tline[i] == "COMPARISON":
                value = comparison(line, tline, i, rowNum)
                string = string + value
                break
            elif tline[i] == "MATH":
                value = str(mathOp(line, tline, i, rowNum))
                string = string + value
                break
            else:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append("Error: Type " + str(tline[i]) + " cannot be printed")
                return returnVals
                raise RuntimeError("Type %r cannot be printed" % (tline[i]))

    print(string)
    returnVals.append(string)


def searchVarValue(name):
    global vars, returnVals, runtimeError
    name = name.strip()
    for variable in vars:
        if variable.name == name:
            return variable.value, variable.dataType

    runtimeError = True
    returnVals.append(runtimeError)
    returnVals.append("Variable " + str(name) + " does not exist")
    return returnVals
    raise RuntimeError("Variable %r does not exist" % (name))


def typeCasting(value, type1, type2, rowNum):
    global returnVals, runtimeError
    if type1 == "NOOB":
        if type2 == "TROOF":
            return False
        else:
            runtimeError = True
            returnVals.append(runtimeError)
            returnVals.append(
                "Encountered error in line "
                + str(rowNum)
                + ", cannot typecast NOOB to "
                + str(type2)
            )
            return returnVals
            raise RuntimeError(
                "Encountered error in line %d, cannot typecast NOOB to %r"
                % (rowNum, type2)
            )
    elif type1 == "NUMBR" or type1 == "NUMBAR":
        match type2:
            case "NUMBAR":
                return float(value)
            case "NUMBR":
                return int(value)
            case "YARN":
                return str(value)
            case "TROOF":
                if value == 0:
                    return "FAIL"
                else:
                    return "WIN"
            case _:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Encountered error in line "
                    + str(rowNum)
                    + ", cannot typecast NUMBR to "
                    + str(type2)
                )
                return returnVals
                raise RuntimeError(
                    "Encountered error in line %d, cannot typecast NUMBR to %r"
                    % (rowNum, type2)
                )
    elif type1 == "TROOF":
        match type2:
            case "NUMBAR":
                if value == "WIN":
                    return 1.0
                else:
                    return 0
            case "NUMBR":
                if value == "WIN":
                    return 1
                else:
                    return 0
            case "YARN":
                return value
            case _:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Encountered error in line "
                    + str(rowNum)
                    + ", cannot typecast TROOF to "
                    + str(type2)
                )
                return returnVals
                raise RuntimeError(
                    "Encoutnered error in line %d, cannot typecast TROOF to %r"
                    % (rowNum, type2)
                )
    elif type1 == "YARN":
        value = value[1:-1]
        match type2:
            case "NUMBR":
                if bool(re.search(r"-?\d(\d)*", value)):
                    return int(value)
                else:
                    runtimeError = True
                    returnVals.append(runtimeError)
                    returnVals.append(
                        "Encountered error in line "
                        + str(rowNum)
                        + ", cannot typecast YARN to "
                        + str(type2)
                    )
                    return returnVals
                    raise RuntimeError(
                        "Encountered error in line %d, cannot typecast YARN to %r"
                        % (rowNum, type2)
                    )
            case "NUMBAR":
                if bool(re.search(r"-?\d(\d)*\.\d(\d)*", value)):
                    return float(value)
                else:
                    runtimeError = True
                    returnVals.append(runtimeError)
                    returnVals.append(
                        "Encountered error in line "
                        + str(rowNum)
                        + ", cannot typecast YARN to "
                        + str(type2)
                    )
                    return returnVals
                    raise RuntimeError(
                        "Encountered error in line %d, cannot typecast YARN to %r"
                        % (rowNum, type2)
                    )
            case "TROOF":
                if value == "":
                    return "FAIL"
                else:
                    return "WIN"
            case _:
                runtimeError = True
                returnVals.append(runtimeError)
                returnVals.append(
                    "Encountered error in line "
                    + str(rowNum)
                    + ", cannot typecast YARN to "
                    + str(type2)
                )
                return returnVals
                raise RuntimeError(
                    "Encountered error in line %d, cannot typecast YARN to %r"
                    % (rowNum, type2)
                )


def printVariables():
    global vars
    for variable in vars:
        print(variable.name)
        print(variable.dataType)
        print(variable.value)
        print("")


def storeVariables(varName, type, newVal):
    global vars, returnVals, runtimeError
    for variable in vars:
        if variable.name == varName:
            variable.dataType = type
            variable.value = newVal
    # runtimeError = True
    # returnVals.append(runtimeError)
    # returnVals.append("Variable " + str(varName) + " does not exizt")
    # return returnVals
    return RuntimeError("Variable %r does not exist")
