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
        path = sys.argv[1]
        f = open(path)
        current_token = ''
        token_type = None
        while True:
            current_line = f.readline()
            if not current_line:
                break
            current_token = ''
            token_type = None
            for current_char in current_line:
                if token_type == 'digit':
                    if current_char.isdigit():
                        current_token += current_char
                    else:
                        print(f'Int({int(current_token)})')
                        current_token = ''
                        token_type = None
                if token_type == 'word':
                    if current_char.isalnum():
                        current_token += current_char
                    else:
                        if current_token in keywords.keys():
                            print(keywords[current_token])
                            current_token = ''
                            token_type = None
                        else:
                            print(f'Ident({current_token})')
                            current_token = ''
                            token_type = None
                if token_type == 'symbol':
                    if current_char == '=' and current_token == ':':
                        current_token += current_char
                    else:
                        print(keywords[current_token])
                        current_token = ''
                        token_type = None
                if token_type == None:
                    if current_char.isdigit():
                        token_type = 'digit'
                        current_token += current_char
                    elif current_char.isalpha():
                        token_type = 'word'
                        current_token += current_char
                    elif current_char in keywords.keys():
                        token_type = 'symbol'
                        current_token += current_char
                    elif current_char.isspace():
                        pass
                    else:
                        print('Unknown')
                        sys.exit(0)
    except EOFError:
        pass
