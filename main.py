import ply.lex as lex

# nested comments /* comment */ and (* comment *)
class Lexer():
    tokens = (
        'TOKEN',
        'START_COMMENT1', 
        'END_COMMENT1', 
        'START_COMMENT2', 
        'END_COMMENT2'
    
    )

    state = [
        ('COMMENT1', 'exclusive'),
        ('COMMENT2', 'exclusive')
    ]

    t_TOKEN = r'[a-zA-Z0-9]'
    t_START_COMMENT1 = r'/\*'
    t_END_COMMENT1 = r'\*/'
    t_START_COMMENT2 = r'\(\*'
    t_END_COMMENT2 = r'\*\)'

    t_ignore = ' \t\n'


    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.depth = 0

    def t_error(self, error):
        error.lexer.skip(1)
    
    def deLexicalAnalysis(self, input):
        self.lexer.input(input)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

s = Lexer()
s.deLexicalAnalysis(r"hello /* bye */ i lovs (* you *)")
    




