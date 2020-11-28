from lark import Lark, Tree

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
    # 输入
    input_file = open("test.c0")
    input_str = input_file.read()
    # 生成语法树
    lark_file = open('C0.lark')
    lark_str = lark_file.read()
    lark = Lark(lark_str)
    parse_tree = lark.parse(input_str)
    print(parse_tree.pretty())
    # 代码生成
    codegen(parse_tree)
    input_file.close()
