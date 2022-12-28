import ply.lex as lex

# nested comments /* comment */ and (* comment *)
class Lexer():

    # Tokens
    tokens = (
        'TOKEN',
        'STARTCOMMENT1', 
        'ENDCOMMENT1', 
        'STARTCOMMENT2', 
        'ENDCOMMENT2'
    
    )

    # States
    states = [
        ('COMMENT1', 'exclusive'),
        ('COMMENT2', 'exclusive')
    ]

    # Ignored characters
    t_ignore = ' \t\n'
    t_COMMENT1_ignore = ' \t\n'
    t_COMMENT2_ignore = ' \t\n'

    def __init__(self):
        self.depth = 0

    # Error handling rule
    def t_error(self, error):
        error.lexer.skip(1)
    
    # Regular expression rules for simple tokens
    def t_TOKEN(self, token):
        r'[a-zA-Z0-9]'
        return token

    # Regular expression rules for comments which start with /*
    def t_STARTCOMMENT1(self, token):
        r'/\*'
        token.lexer.push_state('COMMENT1')
        self.depth += 1
    
    # Regular expression rules for comments which start with (*
    def t_STARTCOMMENT2(self, token):
        r'\(\*'
        token.lexer.push_state('COMMENT2')
        self.depth += 1

    # Regular expression rules for comments which end with */ in INITIAL state
    def t_ENDCOMMENT1(self, token):
        r'\*/'
        print('This end comment has no start comment you needed to use: /* before */')

    # Regular expression rules for comments which end with *) in INITIAL state
    def t_ENDCOMMENT2(self, token):
        r'\*\)'
        print('This end comment has no start comment you needed to use: (* before *)')

    # Error handling rule for comments which start with /*
    def t_COMMENT1_error(self, error):
        error.lexer.skip(1)
    
    # Error handling rule for comments which start with (*
    def t_COMMENT2_error(self, error):
        error.lexer.skip(1)

    # Regular expression rules for COMMENT1 state with STARTCOMMENT1 
    def t_COMMENT1_STARTCOMMENT1(self, token):
        r'/\*'
        token.lexer.push_state('COMMENT1')
        self.depth += 1
    
    # Regular expression rules for COMMENT2 state with STARTCOMMENT2
    def t_COMMENT1_STARTCOMMENT2(self, token):
        r'\(\*'
        token.lexer.push_state('COMMENT2')
        self.depth += 1

    # Regular expression rules for COMMENT2 state with STARTCOMMENT1
    def t_COMMENT2_STARTCOMMENT1(self, token):
        r'/\*'
        token.lexer.push_state('COMMENT1')
        self.depth += 1

    # Regular expression rules for COMMENT2 state with STARTCOMMENT2 
    def t_COMMENT2_STARTCOMMENT2(self, token):
        r'\(\*'
        token.lexer.push_state('COMMENT2')
        self.depth += 1
    
    # Regular expression rules for COMMENT1 state with ENDCOMMENT1 and handling of nested comments with stack and depth
    def t_COMMENT1_ENDCOMMENT1(self, token):
        r'\*/'
        token.lexer.pop_state()
        self.depth -= 1

        if self.depth == 0:
            token.lexer.begin('INITIAL')     
    
    # Regular expression rules for COMMENT2 state with ENDCOMMENT2 and handling of nested comments with stack and depth
    def t_COMMENT1_ENDCOMMENT2(self, token):
        r'\*\)'
        token.lexer.pop_state()
        self.depth -= 1
        print('Wrong comment ending expected: */')

        if self.depth == 0:
            token.lexer.begin('INITIAL')

    # Regular expression rules for COMMENT2 state with ENDCOMMENT1 and handling of nested comments with stack and depth
    def t_COMMENT2_ENDCOMMENT2(self, token):
        r'\*\)'
        token.lexer.pop_state()
        self.depth -= 1

        if self.depth == 0:
            token.lexer.begin('INITIAL')
    
    # Regular expression rules for COMMENT2 state with ENDCOMMENT1 and handling of nested comments with stack and depth
    def t_COMMENT2_ENDCOMMENT1(self, token):
        r'\*/'
        token.lexer.pop_state()
        self.depth -= 1
        print('Wrong comment ending expected: *)')

        if self.depth == 0:
            token.lexer.begin('INITIAL')

    # Function to call the lexer
    def deLexicalAnalysis(self, input):
        self.lexer = lex.lex(module=self)
        self.lexer.input(input)
        
        # Tokenize
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

s = Lexer()

# Output without ERROR
print('Output without ERROR:')
s.deLexicalAnalysis(r"hello (* /* bye nested */ test *) /* something */ dear")

print('---------------------')

# Output with ERROR
print('Output with ERROR:')
s.deLexicalAnalysis(r"hello */ /* bye *) test (* something *)")


