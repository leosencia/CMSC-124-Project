class SyntaxAnalyzer:
    def isVarDec(tokens, row, col, i):
        print("yes")

    def func(self, tokens, row, col):
        i = 0
        word = tokens[i]
        while word == 'COMMENT':
            i += 1

        if word == 'START':
            i += 1 #line2
            word = tokens[i]
            if word == 'WAZZUP':
                #enter variable declaration region
                while word != 'BUHBYE':
                    i += 1
                    isVarDec(tokens, row, col)                    
                    
        else:
            raise RuntimeError('%r unexpected on line %d' % (word, row[i]))