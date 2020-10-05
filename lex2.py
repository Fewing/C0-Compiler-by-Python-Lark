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
        while True:
            current_line = f.readline()
            if not current_line:
                break
            print(current_line)
    except EOFError:
        pass
