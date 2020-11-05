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
    '+': -1, '*': -1, 'i': -1, '(': -1, ')': None, '#': None,
}}

stack = []

if __name__ == "__main__":
    #path = sys.argv[1]
    f = open('input.txt')
    input_str = f.readline()
    i = 0
    stack.append('#')
    while True:
        if stack[len(stack)-1] in m:
            if m[stack[len(stack)-1]][input_str[i]] == 1:
                print('R')
            else:
                stack.append(input_str[i])
                print('I'+input_str[i])
                i += 1
        else:
            if m[stack[len(stack)-2]][input_str[i]] == 1:
                print('R')
            else:
                stack.append(input_str[i])
                print('I'+input_str[i])
                i += 1
