from lark import Tree

import utils.postfunc as postfn
import utils.prefunc as prefn

from utils.table import ident_table


class Generator():
    globaldef = []
    funcdef = [{'name': 0, 'return_slots': 0, 'param_slots': 0, 'loc_slots': 0,
                'instructions': []
                }, ]
    __next_block = True  # 函数传参后，下一个block_stmt不执行

    def codegen(self, tree: Tree):
        if isinstance(tree, Tree):
            if tree.data == 'block_stmt':
                if self.__next_block:
                    prefn.block_stmt(tree)
                else:
                    self.__next_block = True
            if tree.data == 'let_decl_stmt':
                prefn.let_decl_stmt(tree, self.globaldef, self.funcdef)
            if tree.data == 'const_decl_stmt':
                prefn.const_decl_stmt(tree, self.globaldef, self.funcdef)
            if tree.data == 'function':
                prefn.function(tree, self.funcdef)
            if tree.data == 'function_param_list':
                global __next_block
                ident_table.append({})
                self.__next_block = False
            if tree.data == 'function_param':
                prefn.function_param(tree, self.funcdef)
            #前序
            for child in tree.children:
                self.codegen(child)
            #后序
            if tree.data == 'block_stmt':
                postfn.block_stmt(tree)
        else: #叶节点
            pass
