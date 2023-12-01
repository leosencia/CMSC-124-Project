from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer
from SyntaxAnalyzer import SyntaxAnalyzer

if __name__ == '__main__':
    Buffer = Buffer()
    Analyzer = LexicalAnalyzer()
    Syntax = SyntaxAnalyzer()

    # Lists for every list returned list from the function tokenize
    token = []
    lexeme = []
    row = []
    column = []

    # Tokenize and reload of the buffer
    for i in Buffer.load_buffer():
        t, lex, lin, col = Analyzer.tokenize(i)
        token += t
        lexeme += lex
        row += lin
        column += col
    
    print('\nRecognize Tokens: ', token)
    print('\nRecognize Lexems: ', lexeme)
    print('\nRecognize row: ', row)
    print('\nRecognize col: ', column)
    Syntax.program(token, lexeme, row)

