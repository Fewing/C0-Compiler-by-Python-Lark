import sys
from lark import Lark
from utils.generator import Generator
from utils.table import ident_table
from utils.asm import C0ASM

if __name__ == "__main__":
    # 输入
    input_path = sys.argv[1]
    input_file = open(input_path)
    input_str = input_file.read()
    print(input_str)
    # 生成语法树
    lark_file = open('C0-lark/C0.lark',encoding='utf-8')
    lark_str = lark_file.read()
    lark = Lark(lark_str)
    parse_tree = lark.parse(input_str)
    # 代码生成
    gen = Generator()
    gen.codegen(parse_tree)
    #汇编
    c0asm = C0ASM()
    c0asm.asm_globaldef(value_list=gen.globaldef)
    c0asm.asm_functiondef(func_list=gen.funcdef)
    #输出
    obj = c0asm.get()
    output_path = sys.argv[3]
    ouput_file = open(output_path,'wb')
    ouput_file.write(obj)
    input_file.close()
    ouput_file.close()