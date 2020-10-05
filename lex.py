import string


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
    current_token = ''
    token_type = None
    while True:
        current_line = input()
        if not current_line:
            break
        current_token = ''
        token_type = None
        for current_char in current_line:
            if token_type == None:
                if current_char.isdigit():
                    token_type = 'digit'
                    current_token += current_char
                if current_char.isalpha():
                    token_type = 'word'
                    current_token += current_char
                if current_char in keywords.keys():
                    token_type = 'symbol'
                    current_token += current_char
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
            if token_type == 'symbol':
                if current_char.isspace():
                    if current_char in keywords.keys():
                        current_token += current_char
                    if current_token in keywords.keys():
                        print(keywords[current_token])
                        current_token = ''
                        token_type = None
                    
