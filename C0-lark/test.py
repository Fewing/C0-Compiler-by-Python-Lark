from lark import Lark

if __name__ == "__main__":
    input_file = open("test.c0")
    input_str = input_file.read()

    lark_file = open('C0.lark')
    lark_str = lark_file.read()
    lark = Lark(lark_str)

    res = lark.parse(input_str)
    print(res.pretty())

    input_file.close()
