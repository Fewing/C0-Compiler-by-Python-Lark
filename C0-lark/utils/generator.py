from lark import Tree

import utils.postfunc as postfn
import utils.prefunc as prefn

from utils.table import ident_table,func_table


class Generator():
    globaldef = []
    funcdef = [{'name': 0, 'return_slots': 0, 'param_slots': 0, 'loc_slots': 0,
                'instructions': []
                }, ]
    __next_block = True  # 函数传参后，下一个block_stmt不执行
    __exper = False

    def codegen(self, tree: Tree):
        if isinstance(tree, Tree):
            if tree.data == 'block_stmt':
                if self.__next_block:
                    prefn.block_stmt(tree)
                else:
                    self.__next_block = True
            if tree.data == 'let_decl_stmt':
                prefn.let_decl_stmt(tree, self.globaldef, self.funcdef)
                if len(tree.children)==3:
                    self.__exper = True
            if tree.data == 'const_decl_stmt':
                prefn.const_decl_stmt(tree, self.globaldef, self.funcdef)
                if len(tree.children)==3:
                    self.__exper = True
            if tree.data == 'function':
                prefn.function(tree, self.funcdef)
            if tree.data == 'function_param_list':
                ident_table.append({})
                self.__next_block = False
            if tree.data == 'function_param':
                prefn.function_param(tree, self.funcdef)
            if tree.data == 'expr_stmt':
                self.__exper = True
            if tree.data == 'call_expr':
                prefn.call_expr(tree,self.funcdef)
            if tree.data == 'assign_expr':
                prefn.assign_expr(tree,self.funcdef)
            #前序
            for child in tree.children:
                self.codegen(child)
            #后序
            if tree.data == 'expr_stmt':
                self.__exper = False
            if tree.data == 'block_stmt':
                postfn.block_stmt(tree)
            if tree.data == 'let_decl_stmt':
                if len(tree.children) == 3:
                    self.funcdef[-1]['instructions'].append({'ins':'store.64'})
                self.__exper =False
            if tree.data == 'const_decl_stmt':
                self.funcdef[-1]['instructions'].append({'ins':'store.64'})
                self.__exper =False
            if tree.data == 'assign_expr':
                self.funcdef[-1]['instructions'].append({'ins':'store.64'})
            if tree.data == 'call_expr':
                postfn.call_expr(tree,self.funcdef)
            if tree.data == 'add':
                self.funcdef[-1]['instructions'].append({'ins':'add.i'})
            if tree.data == 'sub':
                self.funcdef[-1]['instructions'].append({'ins':'sub.i'})
            if tree.data == 'mul':
                self.funcdef[-1]['instructions'].append({'ins':'mul.i'})
            if tree.data == 'div':
                self.funcdef[-1]['instructions'].append({'ins':'div.i'})
            if tree.data == 'neg':
                self.funcdef[-1]['instructions'].append({'ins':'neg.i'})
        else: #叶节点
            if self.__exper:
                if tree.type == 'NUMBER':
                    self.funcdef[-1]['instructions'].append({'ins':'push','op_64':tree.value})
                if tree.type == 'IDENT':
                    postfn.ident(tree,self.funcdef)
