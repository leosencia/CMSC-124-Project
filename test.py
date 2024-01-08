import re
# arq = open("sample_lolcodes/hello_world.lol", "r")
# text = arq.read()

# # for m in re.finditer(r'(?P<START>^HAI)|(?P<END>KTHXBYE$)|(?P<WAZZUP>WAZZUP)|(?P<BUHBYE>BUHBYE)|(?P<COMMENT> ?BTW .*)|(?P<MULTILINESTART>(OBTW[\w\s]+?(?=TLDR))|(?P<MULTILINEEND>TLDR)', text):
# #     token_type = m.lastgroup
# #     token_lexeme = m.group(token_type)
# #     print(token_type + " lexeme: "+ token_lexeme)
# # print(text)

p = re.compile(r'(?=\n(?:ADDITIONAL|Additional)\n)[\s\S]+?(?<=\n(?:Languages|LANGUAGES)\b)', re.MULTILINE)
test_str = "Academy \nADDITIONAL\nAwards and Recognition: Greek Man of the Year 2011 Stanford PanHellenic Community, American Delegate 2010 Global\nEngagement Summit, Honorary Speaker 2010 SELA Convention, Semi-Finalist 2010 Strauss Foundation Scholarship Program\nComputer Skills: Competency: MATLAB, MySQL/PHP, JavaScript, Objective-C, Git Proficiency: Adobe Creative Suite, Excel\n(highly advanced), PowerPoint, HTML5/CSS3\nLanguages: Fluent English, Advanced Spanish\n\x0c"
print(re.findall(p, test_str))