import wx
import wx.lib.scrolledpanel as scrolled
from Buffer import Buffer
from LexicalAnalyzer import LexicalAnalyzer
from SyntaxAnalyzer import SyntaxAnalyzer

if __name__ == "__main__":
    Buffer = Buffer()
    Analyzer = LexicalAnalyzer()
    Syntax = SyntaxAnalyzer()
    path = None
    display_text = None
    terminal_font_path = "resources/Modeseven-L3n5.ttf"

    # Lists for every list returned list from the function tokenize
    token = []
    lexeme = []
    row = []
    column = []
    txt_ctrl_val = ""
    file_attached = False
    returnVal = []
    variables = []

    # these variables are instantiated early because of scope issues
    app = wx.App()
    icon = wx.Icon("resources/lol.ico")
    frame = wx.Frame(None, title="LOLCode Interpreter", size=(1000, 800))
    frame.SetBackgroundColour("#EFF1F3")
    frame.SetIcon(icon)

    panel = wx.Panel(frame)
    text_editor = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

    main_horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
    left_vertical_box = wx.BoxSizer(wx.VERTICAL)
    right_vertical_box = wx.BoxSizer(wx.VERTICAL)
    left_panel = wx.Panel(panel, size=(200, 200))
    text_editor_box = wx.BoxSizer(wx.VERTICAL)
    left_main_vbox = wx.BoxSizer(wx.VERTICAL)
    left_main_title = wx.StaticText(
        left_panel, label="LEXEMES AND SYMBOLS", style=wx.ALIGN_LEFT
    )
    titles_panel = wx.Panel(left_panel)
    titles2_panel = wx.Panel(left_panel)
    titles_hbox = wx.BoxSizer(wx.HORIZONTAL)
    titles2_hbox = wx.BoxSizer(wx.HORIZONTAL)
    lex_title = wx.StaticText(titles_panel, label="   Lexeme")
    class_title = wx.StaticText(titles_panel, label="Classification")
    ident_title = wx.StaticText(titles2_panel, label="   Identifier")
    val_title = wx.StaticText(titles2_panel, label="Value")
    table_content_scrollpanel = scrolled.ScrolledPanel(left_panel, size=(200, 200))
    table_content_scrollpanel.SetupScrolling()
    table2_content_scrollpanel = scrolled.ScrolledPanel(left_panel, size=(200, 200))
    table2_content_scrollpanel.SetupScrolling()
    table_content_columns = wx.BoxSizer(wx.HORIZONTAL)
    table2_content_columns = wx.BoxSizer(wx.HORIZONTAL)
    table_content_col1 = wx.BoxSizer(wx.VERTICAL)
    table2_content_col1 = wx.BoxSizer(wx.VERTICAL)
    table_content_col2 = wx.BoxSizer(wx.VERTICAL)
    table2_content_col2 = wx.BoxSizer(wx.VERTICAL)
    terminal_panel = wx.Panel(panel)
    terminal_title = wx.StaticText(terminal_panel, label="TERMINAL")
    terminal_box = wx.BoxSizer(wx.VERTICAL)
    terminal_scrollpane = scrolled.ScrolledPanel(terminal_panel, size=(200, 200))
    terminal_scrollpane.SetupScrolling()
    terminal_context_box = wx.BoxSizer(wx.VERTICAL)
    execute_button_box = wx.BoxSizer(wx.VERTICAL)
    execute_button = wx.Button(panel, label="EXECUTE")

    wx.Font.AddPrivateFont(terminal_font_path)

    terminal_font = wx.Font(
        10,
        wx.FONTFAMILY_DEFAULT,
        wx.FONTSTYLE_NORMAL,
        wx.FONTWEIGHT_NORMAL,
        False,
        "ModeSeven",
        encoding=wx.FONTENCODING_DEFAULT,
    )

    tables_font = panel.GetFont()
    tables_font.SetPointSize(8)
    tables_font.SetWeight(wx.FONTWEIGHT_NORMAL)

    line = wx.StaticLine(terminal_panel, size=(400, -1), style=wx.LI_HORIZONTAL)

    def on_attach_file_button(event):
        global path, txt_ctrl_val, text_editor, file_attached, returnVal, variables
        variables = []
        returnVal = []
        path = None
        with wx.FileDialog(
            frame,
            "Open",
            wildcard="All files (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()

            print(f"Selected file: {path}")
            returnVal = start(path, 2)
            text_editor.SetValue("".join(returnVal[0]))
            returnVal = None

        file_attached = True

    def on_execute_button(event):
        global variables
        variables = []
        # clear terminal_context_box
        terminal_context_box.Clear(True)
        table2_content_col1.Clear(True)
        table2_content_col2.Clear(True)
        if file_attached == True:
            # if a file is attached, editing the text editor will affect the execution
            curr_val = text_editor.GetValue()
            # print(curr_val)

            with open(path, "w") as file:
                file.write(curr_val)

            # print("Executing in mode 1")
            returnVal = start(path, 1)
            # print(returnVal)
            if returnVal[0][0] == False:
                print("HEREEE")
                print(returnVal)
                terminal_content = []
                for i in range(len(returnVal[0])):
                    if type(returnVal[0][i]) == str:
                        terminal_content.append(returnVal[0][i])
                    if type(returnVal[0][i]) == list:
                        for j in range(len(returnVal[0][i])):
                            # print(returnVal[0][i][j].name)
                            # print("Value: ", returnVal[0][i][j].value)
                            # print("Data type: ", returnVal[0][i][j].dataType)
                            var = []
                            var.append(returnVal[0][i][j].name)
                            var.append(returnVal[0][i][j].value)
                            variables.append(var)

                joined_terminal_content = "\n".join(terminal_content)
                start_str = '> lolcode -u "' + path + '"\n'
                start_text = wx.StaticText(terminal_scrollpane, label=start_str)
                start_text.SetFont(terminal_font)
                start_text.SetForegroundColour("#98ddeb")
                joined_text = wx.StaticText(
                    terminal_scrollpane, label=joined_terminal_content
                )
                joined_text.SetFont(terminal_font)
                joined_text.SetForegroundColour("#FFFFFF")
                terminal_context_box.Add(start_text, 0, wx.EXPAND | wx.ALL, 10)
                terminal_context_box.Add(joined_text, 0, wx.EXPAND | wx.ALL, 10)
                returnVal = []
            else:
                print("KKKK")
                print(returnVal)
                terminal_content = []
                for i in range(len(returnVal[0])):
                    if type(returnVal[0][i]) == str:
                        terminal_content.append(returnVal[0][i])
                    if type(returnVal[0][i]) == list:
                        for j in range(len(returnVal[0][i])):
                            var = []
                            var.append(returnVal[0][i][j].name)
                            var.append(returnVal[0][i][j].value)
                            variables.append(var)
                # print(terminal_content)
                joined_terminal_content = "\n".join(terminal_content)
                start_str = '> lolcode -u "' + path + '"\n'
                start_text = wx.StaticText(terminal_scrollpane, label=start_str)
                start_text.SetFont(terminal_font)
                start_text.SetForegroundColour("#98ddeb")
                terminal_text = wx.StaticText(
                    terminal_scrollpane, label=joined_terminal_content
                )
                terminal_text.SetFont(terminal_font)
                terminal_text.SetForegroundColour("#FFFFFF")
                terminal_context_box.Add(terminal_text, 1, wx.EXPAND | wx.ALL, 20)
                returnVal = []
        else:
            pass
        print(variables)
        combined_col = ""
        combined_col2 = ""
        print(variables)
        for i in range(len(variables)):
            ident = variables[i][0].strip()  # remove trailing spaces
            if type(variables[i][1]) == str:
                val = variables[i][1].strip()  # remove trailing spaces
            else:
                val = str(variables[i][1])
            if i == 0:
                combined_col = combined_col + ident
                combined_col2 = combined_col2 + val
            else:
                combined_col = combined_col + "\n" + ident
                combined_col2 = combined_col2 + "\n" + val
        print("combined col: ", combined_col)
        print("combined col2: ", combined_col2)
        identCol = wx.StaticText(table2_content_scrollpanel, label=combined_col)
        identCol.SetFont(tables_font)
        identCol.SetForegroundColour("#FFFFFF")
        table2_content_col1.Add(identCol, 0, wx.ALIGN_LEFT, 0)

        valCol = wx.StaticText(table2_content_scrollpanel, label=combined_col2)
        valCol.SetFont(tables_font)
        valCol.SetForegroundColour("#FFFFFF")
        table2_content_col2.Add(valCol, 0, wx.ALIGN_LEFT, 0)

    def start(path, mode):
        global token, lexeme, row, column, display_text
        if mode == 2:
            # clear the lists
            token.clear()
            lexeme.clear()
            row.clear()
            column.clear()
            table_content_col1.Clear(True)
            table_content_col2.Clear(True)

            # Tokenize and reload of the buffer
            display_text = list(Buffer.load_buffer(path, mode))
            returnValues = [display_text]
            for i in display_text:
                t, lex, lin, col = Analyzer.tokenize(i)
                if t == False:
                    continue
                else:
                    token += t
                    lexeme += lex
                    row += lin
                    column += col
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
            table_content_col1.Add(lexCol, 0, wx.ALIGN_LEFT, 0)

            combined_col2 = ""
            for i in range(len(token)):
                toke = token[i].strip()  # remove trailing spaces
                if i == 0:
                    combined_col2 = combined_col2 + toke
                else:
                    combined_col2 = combined_col2 + "\n" + toke
            lexCol2 = wx.StaticText(table_content_scrollpanel, label=combined_col2)
            lexCol2.SetFont(tables_font)
            lexCol2.SetForegroundColour("#FFFFFF")
            table_content_col2.Add(lexCol2, 0, wx.ALIGN_LEFT, 0)
        elif mode == 1:
            # print(mode)
            # clear the lists
            token.clear()
            lexeme.clear()
            row.clear()
            column.clear()
            # iterate through the list of lines returned by the buffer
            for i in Buffer.load_buffer(path, mode):
                t, lex, lin, col = Analyzer.tokenize(i)
                if t == False:
                    retVals = [t, lex]
                    returnValues = [retVals]
                    return returnValues
                else:
                    token += t
                    lexeme += lex
                    row += lin
                    column += col

            retVals = Syntax.program(token, lexeme, row)
            returnValues = [retVals]
        return returnValues

    # rest of GUI-related code

    left_panel.SetBackgroundColour("#032b43")
    main_horizontal_box.Add(left_panel, 1, wx.EXPAND)

    # main_horizontal_box.Add(left_vertical_box, 1, wx.EXPAND)
    # inner_left_panel = wx.Panel(panel, size=(200, 200))
    # inner_left_panel.SetBackgroundColour("#141E46")
    # add inner left panel to left vertical box
    # left_vertical_box.Add(inner_left_panel, 1, wx.EXPAND)

    main_horizontal_box.Add(right_vertical_box, 3, wx.EXPAND)

    # add text editor box to right vertical box
    right_vertical_box.Add(text_editor_box, 2, wx.EXPAND)
    right_vertical_box.Add(execute_button_box, 0, wx.EXPAND)
    right_vertical_box.Add(terminal_panel, 1, wx.EXPAND)

    # adding the attach file button
    attach_file_button = wx.Button(panel, size=(30, 30))
    attach_icon = wx.Bitmap("resources/attach.ico")
    attach_icon = attach_icon.ConvertToImage()
    attach_icon = attach_icon.Rescale(20, 20, wx.IMAGE_QUALITY_HIGH)
    attach_file_button.SetBitmap(attach_icon)
    attach_file_button.SetBackgroundColour("#FFFFFF")
    # binding button to functionality
    attach_file_button.Bind(wx.EVT_BUTTON, on_attach_file_button)
    # add attach button to text editor box
    text_editor_box.Add(attach_file_button, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

    # text editor widget
    text_editor.SetValue(txt_ctrl_val)
    text_editor.SetBackgroundColour("#FFFFFF")
    # add text editor to text editor box
    text_editor_box.Add(text_editor, 1, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 20)

    execute_button_box.Add(
        execute_button, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10
    )
    # bind execute button to functionality
    execute_button.Bind(wx.EVT_BUTTON, on_execute_button)

    headers_font = panel.GetFont()
    headers_font.SetPointSize(8)
    headers_font.SetWeight(wx.FONTWEIGHT_BOLD)

    execute_button.SetFont(headers_font)

    table_titles_font = panel.GetFont()
    table_titles_font.SetPointSize(8)
    table_titles_font.SetWeight(wx.FONTWEIGHT_SEMIBOLD)

    left_panel.SetSizer(left_main_vbox)

    left_main_title.SetForegroundColour("#FFFFFF")
    left_main_title.SetFont(headers_font)
    left_main_vbox.Add(left_main_title, 0, wx.ALIGN_CENTER | wx.ALL, 10)

    # titles1_hbox = wx.BoxSizer(wx.HORIZONTAL)
    # left_main_vbox.Add(titles1_hbox, 1, wx.ALL, 10)

    titles_panel.SetBackgroundColour("#62929e")
    titles2_panel.SetBackgroundColour("#62929e")
    left_main_vbox.Add(titles_panel, 0, wx.EXPAND | wx.ALL, 0)

    titles_panel.SetSizer(titles_hbox)
    titles2_panel.SetSizer(titles2_hbox)

    lex_title.SetForegroundColour("#FFFFFF")
    class_title.SetForegroundColour("#FFFFFF")
    ident_title.SetForegroundColour("#FFFFFF")
    val_title.SetForegroundColour("#FFFFFF")
    lex_title.SetFont(table_titles_font)
    class_title.SetFont(table_titles_font)
    ident_title.SetFont(table_titles_font)
    val_title.SetFont(table_titles_font)
    titles_hbox.Add(lex_title, 1, wx.ALIGN_LEFT | wx.ALL, 8)
    titles_hbox.Add(class_title, 1, wx.ALIGN_LEFT | wx.ALL, 8)
    titles2_hbox.Add(ident_title, 1, wx.ALIGN_LEFT | wx.ALL, 8)
    titles2_hbox.Add(val_title, 1, wx.ALIGN_LEFT | wx.ALL, 8)
    left_main_vbox.Add(table_content_scrollpanel, 2, wx.EXPAND | wx.ALL, 10)
    left_main_vbox.Add(titles2_panel, 0, wx.EXPAND | wx.ALL, 0)
    left_main_vbox.Add(table2_content_scrollpanel, 1, wx.EXPAND | wx.ALL, 10)
    table_content_scrollpanel.SetSizer(table_content_columns)
    table2_content_scrollpanel.SetSizer(table2_content_columns)
    table_content_columns.Add(table_content_col1, 1, wx.EXPAND | wx.ALL, 10)
    table_content_columns.Add(table_content_col2, 1, wx.EXPAND | wx.ALL, 10)
    table2_content_columns.Add(table2_content_col1, 1, wx.EXPAND | wx.ALL, 10)
    table2_content_columns.Add(table2_content_col2, 1, wx.EXPAND | wx.ALL, 10)
    # terminal_box.Add(terminal_panel, 1, wx.EXPAND | wx.ALL, 0)
    terminal_panel.SetBackgroundColour("#55828B")
    terminal_panel.SetSizer(terminal_box)
    terminal_box.Add(terminal_title, 0, wx.LEFT | wx.ALL, 10)
    terminal_title.SetForegroundColour("#FFFFFF")
    terminal_title.SetFont(terminal_font)
    terminal_box.Add(line, 0, wx.EXPAND | wx.ALL, 0)
    terminal_box.Add(terminal_scrollpane, 1, wx.EXPAND | wx.ALL, 10)
    terminal_scrollpane.SetSizer(terminal_context_box)
    panel.SetSizer(main_horizontal_box)
    frame.Show()
    app.MainLoop()
