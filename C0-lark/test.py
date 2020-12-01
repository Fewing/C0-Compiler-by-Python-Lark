import json
from lark import Lark
from utils.generator import Generator
from utils.table import ident_table
from utils.asm import C0ASM

if __name__ == "__main__":
    # 输入
    input_file = open("test.c0",encoding='utf-8')
    outpt_file = open("test.o",'wb')
    input_str = input_file.read()
    # 生成语法树
    lark_file = open('C0.lark',encoding='utf-8')
    lark_str = lark_file.read()
    lark = Lark(lark_str)
    parse_tree = lark.parse(input_str)
    #print(parse_tree.pretty())
    # 代码生成
    gen = Generator()
    gen.codegen(parse_tree)
    print(json.dumps(gen.globaldef, indent=4, sort_keys=True))
    print(json.dumps(gen.funcdef, indent=4, sort_keys=True))
    #汇编
    c0asm = C0ASM()
    c0asm.asm_globaldef(value_list=gen.globaldef)
    c0asm.asm_functiondef(func_list=gen.funcdef)
    #输出
    obj = c0asm.get()
    outpt_file.write(obj)
    input_file.close()
