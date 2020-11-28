from lark import Lark ,Tree
import sys

import utils.postfunc as postfn
import utils.prefunc as prefn

def codegen(tree: Tree):
    if isinstance(tree, Tree):
        if tree.data == 'block_stmt':
            prefn.block_stmt(tree)
        if tree.data == 'let_decl_stmt':
            prefn.let_decl_stmt(tree)
        if tree.data == 'const_decl_stmt':
            prefn.const_decl_stmt(tree)
        if tree.data == 'function':
            prefn.function(tree)
        for child in tree.children:
            codegen(child)
        if tree.data == 'block_stmt':
            postfn.block_stmt(tree)
    else:
        pass

if __name__ == "__main__":
    input_path = sys.argv[1]
    input_file = open(input_path)
    input_str = input_file.read()

    output_path = sys.argv[3]
    ouput_file = open(output_path,'w')

    lark_file = open('C0-lark/C0.lark')
    lark_str = lark_file.read()
    lark = Lark(lark_str)

    parse_tree = lark.parse(input_str)
    codegen(parse_tree)
    ouput_file.write(parse_tree.pretty())

    input_file.close()
    ouput_file.close()