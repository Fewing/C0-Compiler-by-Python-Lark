keywords = {}
symbols = {}
types = {}
keywords['fn'] = 'FN'
keywords['let'] = 'LET'
keywords['const'] = 'CONST'
keywords['as'] = 'AS'
keywords['while'] = 'WHILE'
keywords['if'] = 'IF'
keywords['else'] = 'ELSE'
keywords['return'] = 'RETURN'

symbols['+'] = 'PLUS'
symbols['-'] = 'MINUS'
symbols['*'] = 'MUL'
symbols['/'] = 'DIV'
symbols['='] = 'ASSIGN'
symbols['=='] = 'EQ'
symbols['!='] = 'NEQ'
symbols['<'] = 'LT'
symbols['>'] = 'GT'
symbols['<='] = 'LE'
symbols['>='] = 'GE'
symbols['('] = 'L_PAREN'
symbols[')'] = 'R_PAREN'
symbols['{'] = 'L_BRACE'
symbols['}'] = 'R_BRACE'
symbols['->'] = 'ARROW'
symbols[','] = 'COMMA'
symbols[':'] = 'COLON'
symbols[':'] = 'SEMICOLON'


def get_token_list(src_str:str):
    ans = []
    for current_char in src_str:
        ans.append({
            'type':'INT',
            'value':current_char
        })
    return ans

if __name__ == "__main__":
    pass