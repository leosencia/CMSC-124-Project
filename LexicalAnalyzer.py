PATH = "sample_lolcodes/"
import re


# Taken from https://github.com/christianrfg/lexical-analyzer
class LexicalAnalyzer:
    lin_num = 1

    def tokenize(self, code):
        # doesn't catch wrong vars
        rules = [
            ("START", r"^HAI"),
            ("END", r"KTHXBYE$"),
            ("WAZZUP", r"WAZZUP"),
            ("BUHBYE", r"BUHBYE"),
            ("COMMENT", r" ?BTW .*"),
            ("MULTILINESTART", r"(?=\n(?:OBTW)\n)[\s\S]+?(?<=\n(?:TLDR)\b)"),
            ("MULTILINEEND", r"TLDR"),
            ("VAR_DEC", r"I HAS A"),
            ("INPUT", r"GIMMEH"),
            ("ITZ", r"ITZ"),
            ("INLOOP", r"IM IN YR"),
            ("INCR", r"UPPIN YR"),
            ("DECR", r"NERFIN YR"),
            ("WILE", r"WILE"),
            ("TIL", r"TIL"),
            ("OUTLOOP", r"IM OUTTA YR"),
            ("IFELSE", r"O RLY\?"),
            ("IFTRUE", r"YA RLY"),
            ("IFFALSE", r"NO WAI"),
            ("ENDIFELSE", r"OIC"),
            ("R", r"R"),
            ("RECASTMAGIC", r"IS NOW A"),
            ("CONCAT", r"SMOOSH"),
            ("PRINT", r"VISIBLE"),
            ("TYPECAST", r"MAEK"),
            ("RECAST", r"IS NOW A"),
            ("BOOL_OPER", r"(BOTH OF|EITHER OF|WON OF|NOT|ALL OF|ANY OF)"),
            (
                "MATH",
                r"(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF)",
            ),
            ("COMPARISON", r"(BOTH SAEM|DIFFRINT)"),
            ("AN", r"AN"),
            ("YARN", r'"[^"]*"'),
            ("NUMBAR", r"-?\d(\d)*\.\d(\d)*"),  # float const
            ("TROOF", r"(WIN|FAIL)"),
            ("NUMBR", r"-?\d(\d)*"),  # int
            ("DATA_TYPE", r"(NOOB|TROOF|NUMBAR|NUMBR|YARN)"),
            ("VARIABLE", r"[a-zA-Z]\w* ?"),
            ("NEWLINE", r"\n"),  # NEW LINE
            ("SKIP", r"[ \t]+"),
            ("MISMATCH", r"."),
        ]
        tokens_join = "|".join("(?P<%s>%s)" % x for x in rules)
        print(tokens_join)
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

            if token_type == "NEWLINE":
                lin_start = m.end()
                self.lin_num += 1
            elif token_type == "SKIP":
                continue
            elif token_type == "MISMATCH":
                error = (
                    str("ERROR: " + token_lexeme[0])
                    + " unexpected on line "
                    + str(self.lin_num)
                )
                return False, error, False, False
                # raise RuntimeError(
                #     "%r unexpected on line %d" % (token_lexeme, self.lin_num)
                # )
            else:
                col = m.start() - lin_start
                column.append(col)
                token.append(token_type)
                lexeme.append(token_lexeme)
                row.append(self.lin_num)
                # To print information about a Token
                # print(
                #     "Token = {0}, Lexeme = '{1}', Row = {2}, Column = {3}".format(
                #         token_type, token_lexeme, self.lin_num, col
                #     )
                # )

        return token, lexeme, row, column
