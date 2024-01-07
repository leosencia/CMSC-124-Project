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

    # these variables are instantiated early because of scope issues
    app = wx.App()
    icon = wx.Icon("resources/lol.ico")
    frame = wx.Frame(None, title="LOLCode Interpreter", size=(1000, 800))
    frame.SetBackgroundColour("#EFF1F3")
    frame.SetIcon(icon)

    panel = wx.Panel(frame)
    text_editor = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

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
    titles_hbox = wx.BoxSizer(wx.HORIZONTAL)
    lex_title = wx.StaticText(titles_panel, label="Lexeme")
    class_title = wx.StaticText(titles_panel, label="Classification")
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

    line = wx.StaticLine(terminal_panel, size=(400, -1), style=wx.LI_HORIZONTAL)

    def on_attach_file_button(event):
        global path, txt_ctrl_val, text_editor, file_attached
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
            returnVal = start(path)
            text_editor.SetValue("".join(returnVal[0]))
            if returnVal[1][0] == False:
                print("HEREEE")
                print(returnVal[1])
                terminal_content = returnVal[1]
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
                terminal_context_box.Add(joined_text, 1, wx.EXPAND | wx.ALL, 10)
            else:
                print("HEREEE")
                print(returnVal[1])
                terminal_content = returnVal[1]
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
                terminal_context_box.Add(joined_text, 1, wx.EXPAND | wx.ALL, 10)
        file_attached = True

    def on_execute_button(event):
        pass

    def start(path):
        global token, lexeme, row, column, display_text
        # Tokenize and reload of the buffer
        display_text = list(Buffer.load_buffer(path))
        # clear the lists
        token.clear()
        lexeme.clear()
        row.clear()
        column.clear()
        # iterate through the list of lines returned by the buffer
        for i in display_text:
            t, lex, lin, col = Analyzer.tokenize(i)
            token += t
            lexeme += lex
            row += lin
            column += col

        print("\nRecognize Tokens: ", token)
        print("\nRecognize Lexems: ", lexeme)
        # print('\nRecognize row: ', row)
        # print('\nRecognize col: ', column)
        retVals = Syntax.program(token, lexeme, row)
        returnValues = [display_text, retVals]
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
    left_main_vbox.Add(titles_panel, 0, wx.EXPAND | wx.ALL, 0)

    titles_panel.SetSizer(titles_hbox)

    lex_title.SetForegroundColour("#FFFFFF")
    class_title.SetForegroundColour("#FFFFFF")
    lex_title.SetFont(table_titles_font)
    class_title.SetFont(table_titles_font)
    titles_hbox.Add(lex_title, 1, wx.ALIGN_CENTER | wx.ALL, 5)
    titles_hbox.Add(class_title, 1, wx.ALIGN_CENTER | wx.ALL, 5)

    # terminal_box.Add(terminal_panel, 1, wx.EXPAND | wx.ALL, 0)
    terminal_panel.SetBackgroundColour("#55828B")
    terminal_panel.SetSizer(terminal_box)
    terminal_box.Add(terminal_title, 0, wx.LEFT | wx.ALL, 10)
    terminal_title.SetForegroundColour("#FFFFFF")
    terminal_title.SetFont(terminal_font)
    terminal_box.Add(line, 0, wx.EXPAND | wx.ALL, 0)
    terminal_box.Add(terminal_scrollpane, 0, wx.EXPAND | wx.ALL, 10)
    terminal_scrollpane.SetSizer(terminal_context_box)
    panel.SetSizer(main_horizontal_box)
    frame.Show()
    app.MainLoop()
