PATH = "sample_lolcodes/"
import re
#Taken from https://github.com/christianrfg/lexical-analyzer
class LexicalAnalyzer:
    lin_num = 1
    def tokenize(self, code):
        rules = [
                ('START', r'^HAI'),
                ('END', r'KTHXBYE$'),
                ('COMMENT', r' BTW .*'),
                ('VAR_DEC', r'I HAS A'),
                ('ITZ', r'ITZ'),
                ('PRINT', r'VISIBLE'),
                ('STRING', r'"[^"]*"'),
                ('VARIABLE', r'[a-zA-Z]\w*'),
                ('FLOAT_CONST', r'-?\d(\d)*\.\d(\d)*'),
                ('INTEGER_CONST', r'-?\d(\d)*'),
                ]
        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        # print(code + "==========")
        lin_start = 0

        # Lists of output for the program
        token = []
        lexeme = []
        row = []
        column = []

        # It analyzes the code to find the lexemes and their respective Tokens
        for m in re.finditer(tokens_join, code):
            token_type = m.lastgroup
            token_lexeme = m.group(token_type)

            if token_type == 'NEWLINE':
                lin_start = m.end()
                self.lin_num += 1
            elif token_type == 'SKIP':
                continue
            elif token_type == 'MISMATCH':
                raise RuntimeError('%r unexpected on line %d' % (token_lexeme, self.lin_num))
            else:
                    col = m.start() - lin_start
                    column.append(col)
                    token.append(token_type)
                    lexeme.append(token_lexeme)
                    row.append(self.lin_num)
                    # To print information about a Token
                    print('Token = {0}, Lexeme = \'{1}\', Row = {2}, Column = {3}'.format(token_type, token_lexeme, self.lin_num, col))

        return token, lexeme, row, column
        