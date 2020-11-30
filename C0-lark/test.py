import json
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
    # 代码生成
    gen = Generator()
    gen.codegen(parse_tree)
    print(json.dumps(gen.globaldef, indent=4, sort_keys=True))
    print(json.dumps(gen.funcdef, indent=4, sort_keys=True))
    input_file.close()
