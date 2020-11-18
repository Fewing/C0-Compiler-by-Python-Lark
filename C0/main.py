from compiler import lex

if __name__ == "__main__":
    f = open('C:/Users/yangz/Desktop/compile_homework/C0/input.c0')
    src = f.read()
    ans = lex.get_token_list(src)
    print(ans)