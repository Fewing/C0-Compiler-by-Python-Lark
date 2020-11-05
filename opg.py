import string
import sys


m = {'+': {
    '+': 1, '*': -1, 'i': -1, '(': -1, ')': 1, '#': 1,
}, '*': {
    '+': 1, '*': 1, 'i': -1, '(': -1, ')': 1, '#': 1,
}, 'i': {
    '+': 1, '*': 1, 'i': None, '(': None, ')': 1, '#': 1,
}, '(': {
    '+': -1, '*': -1, 'i': -1, '(': -1, ')': 0, '#': None,
}, ')': {
    '+': 1, '*': 1, 'i': None, '(': None, ')': 1, '#': 1,
}, '#': {
    '+': -1, '*': -1, 'i': -1, '(': -1, ')': None, '#': 0,
}}

stack = []

if __name__ == "__main__":
    path = sys.argv[1]
    f = open(path)
    input_str = f.readline()
    i = 0
    input_str += '#'
    input_str = input_str.replace('\n','')
    input_str = input_str.replace('\r','')
    stack.append('#')
    while True:
        if stack[len(stack)-1] in m:
            if m[stack[len(stack)-1]][input_str[i]] == 1:
                if stack[len(stack)-1] == 'i':
                    print('R')
                    stack.pop()
                    stack.append('E')
                elif stack[len(stack)-1] == ')' and len(stack) >= 3 and stack[len(stack)-2] == 'E' and stack[len(stack)-3] == '(':
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    print('R')
                    stack.append('E')
                else:
                    print('RE')
                    break
            elif m[stack[len(stack)-1]][input_str[i]] == -1 or m[stack[len(stack)-1]][input_str[i]] == 0:
                stack.append(input_str[i])
                print('I'+input_str[i])
                i += 1
            else:
                print('E')
                break
        else:
            if m[stack[len(stack)-2]][input_str[i]] == 1:
                if (stack[len(stack)-2] == '+' or stack[len(stack)-2] == '*') and len(stack) >= 3 and stack[len(stack)-1] == 'E' and stack[len(stack)-3] == 'E':
                    stack.pop()
                    stack.pop()
                    stack.pop()
                    print('R')
                    stack.append('E')
                else:
                    print('RE')
                    break
            elif m[stack[len(stack)-2]][input_str[i]] == -1 or m[stack[len(stack)-2]][input_str[i]] == 0:
                stack.append(input_str[i])
                if input_str[i] == '#':
                    break
                print('I'+input_str[i])
                i += 1
            else:
                print('E')
                break
    f.close()
