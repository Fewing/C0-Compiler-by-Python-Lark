import string
import sys


keywords = {}
keywords['BEGIN'] = 'Begin'
keywords['END'] = 'End'
keywords['FOR'] = 'For'
keywords['IF'] = 'If'
keywords['THEN'] = 'Then'
keywords['ELSE'] = 'Else'
keywords[':'] = 'Colon'
keywords['+'] = 'Plus'
keywords['*'] = 'Star'
keywords[','] = 'Comma'
keywords['('] = 'LParenthesis'
keywords[')'] = 'RParenthesis'
keywords[':='] = 'Assign'


if __name__ == "__main__":
    try:
        path = sys.argv[0]
        f = open(path)
        while True:
            current_line = f.readline()
            if not current_line:
                break
            token_list = current_line.split()
            for token in token_list:
                if token in keywords.keys():
                    print(keywords[token])
                elif token.isdigit():
                    print(f'Int({int(token)})')
                elif token[0].isalpha() and token.isalnum():
                    print(f'Ident({token})')
                elif token[0].isdigit() and token.isalnum():
                    for ch in token:
                        if ch.isalpha():
                            start = token.find(ch)
                            print(f'Int({int(token[:start])})')
                            print(f'Ident({token[start:]})')
                            break
                elif token.isspace():
                    pass
                else:
                    break
    except EOFError:
        pass
