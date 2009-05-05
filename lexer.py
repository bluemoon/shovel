import ply.lex as lex
class DirtLexer:
    def __init__(self):
        self.IndentationStack = [0]
    Reserved = {
        'if' : 'IF',
        'then' : 'THEN',
        'else' : 'ELSE',
        'while' : 'WHILE',
        'print' : 'PRINT',
        }
    # List of token names.   This is always required
    tokens = (
        'INDENT',
        'BLOCK',
        'FUNCTION',
        'BLOCKWUSE',
        'BVARIABLE',
        ) #+ list(Reserved.values())
    
    states = (
        ('block','inclusive'),
        )


    # Regular expression rules for simple tokens
    
    #t_INDENT      = r'(\s|\t)'
    t_LPAREN      = r'\('
    t_RPAREN      = r'\)'
    t_LBRACKET    = r'\['
    t_RBRACKET    = r'\]'
    t_LCURLYB     = r'\{'
    t_RCURLYB     = r'\}'
    #t_BLOCK       = r'\[a-zA-Z]*\:'
    #t_BLOCKWUSE   = r'\[a-zA-Z]*\[[A-Za-z0-9\.]*\]\:'
    #t_BVARIABLE   = r'\{[a-zA-Z0-9\:]*\}'

    
    t_ignore_COMMENT = r'\#.*'

    def IndentClevel(self):
       return self.IndentationStack[-1] 
    def t_INDENT(t):
        r'(\s*|\t)'
        CurrentLevel = self.IndentationStack[-1]
        NewLevel = len(T.value)

        if NewLevel > CurrentLevel:
            self.IndentationStack.append(newLevel)
        elif NewLevel < CurrentLevel:
            while NewLevel < CurrentLevel:
                self.IndentationStack.pop()
                     
                
    # BLOCK STATE
    def t_block_start(t):
        r'\[a-zA-Z]*\:'
        t.lexer.BlockStart = t.lexer.lexpos
        t.lexer.BlockLevel = 1
        t.lexer.begin('block')
    def t_block_open(t):
        r'\[a-zA-Z]*\:'
        t.lexer.BlockLevel = 1
    def t_block_close(t):
        pass
    
    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
    # Error handling rule
    def t_error(t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

