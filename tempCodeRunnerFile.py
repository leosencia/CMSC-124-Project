combined_col = ""
            for i in range(len(lexeme)):
                lex = lexeme[i].strip()  # remove trailing spaces
                if i == 0:
                    combined_col = combined_col + lex
                else:
                    combined_col = combined_col + "\n" + lex
            lexCol = wx.StaticText(table_content_scrollpanel, label=combined_col)
            lexCol.SetFont(tables_font)
            lexCol.SetForegroundColour("#FFFFFF")
            table_content_col1.Add(lexCol, 0, wx.ALIGN_LEFT, 10)