from lark import Lark
from utils.generator import Generator
from utils.table import ident_table

if __name__ == "__main__":
    # 输入
    input_file = open("test.c0")
    input_str = input_file.read()
    # 生成语法树
    lark_file = open('C0.lark')
    lark_str = lark_file.read()
    lark = Lark(lark_str)
    parse_tree = lark.parse(input_str)
    #print(parse_tree.pretty())
    # 代码生成4
    gen = Generator()
    gen.codegen(parse_tree)
    print(gen.globaldef)
    print(gen.funcdef)
    input_file.close()
