from lark import Tree

import utils.postfunc as postfn
import utils.prefunc as prefn

from utils.table import ident_table, func_table


class Generator():
    globaldef = [{
        "is_const": 1,
        "type": "string",
        "value": "_start"
    }, ]
    funcdef = [{'name': 0, 'return_slots': 0, 'param_slots': 0, 'loc_slots': 0,
                'instructions': []
                }, ]
    __next_block = True  # 函数传参后，下一个block_stmt不执行
    __if_block = 0  # if语句块嵌套层数
    __else_block = 0  # else语句块
    __while_block = 0  # while语句块嵌套层数

    def codegen(self, tree: Tree):
        if isinstance(tree, Tree):
            # 前序
            if tree.data == 'block_stmt':
                if self.__next_block:
                    prefn.block_stmt(tree)
                else:
                    self.__next_block = True
            if tree.data == 'if_block_stmt':
                prefn.block_stmt(tree)
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'br.true', 'op_32': 1})
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'br', 'op_32': 0, 'fill': True})
            if tree.data == 'while_block_stmt':
                prefn.block_stmt(tree)
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'br.true', 'op_32': 1})
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'br', 'op_32': 0, 'fill': True})
            if tree.data == 'let_decl_stmt':
                prefn.let_decl_stmt(tree, self.globaldef, self.funcdef)
            if tree.data == 'const_decl_stmt':
                prefn.const_decl_stmt(tree, self.globaldef, self.funcdef)
            if tree.data == 'return_stmt':
                prefn.return_stmt(tree, self.funcdef)
            if tree.data == 'function':
                prefn.function(tree, self.funcdef, self.globaldef)
            if tree.data == 'function_param_list':
                ident_table.append({})
                self.__next_block = False
            if tree.data == 'function_param':
                prefn.function_param(tree, self.funcdef)
            if tree.data == 'call_expr':
                prefn.call_expr(tree, self.funcdef)
            if tree.data == 'assign_expr':
                prefn.assign_expr(tree, self.funcdef)
            if tree.data == 'if_stmt':
                self.__if_block += 1
                tree.children[1].data = 'if_block_stmt'
                if len(tree.children) == 3:
                    if tree.children[2].data == 'if_stmt':
                        tree.children[2].data = 'elif_stmt'
                    else:
                        tree.children[2].data = 'else_stmt'
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'br', 'op_32': 0, 'if_start': True})
            if tree.data == 'elif_stmt':
                tree.children[1].data = 'if_block_stmt'
                if len(tree.children) == 3:
                    if tree.children[2].data == 'if_stmt':
                        tree.children[2].data = 'elif_stmt'
                    else:
                        tree.children[2].data = 'else_stmt'
            if tree.data == 'while_stmt':
                self.__while_block += 1
                tree.children[1].data = 'while_block_stmt'
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'br', 'op_32': 0, 'while_start': True})
            for child in tree.children:
                self.codegen(child)
            # 后序
            if tree.data == 'program':
                self.funcdef[0]['instructions'].append(
                    {'ins': 'stackalloc', 'op_32': self.funcdef[func_table['main']['loc']]['return_slots']})
                self.funcdef[0]['instructions'].append(
                    {'ins': 'call', 'op_32': func_table['main']['loc']})
            if tree.data == 'function':
                postfn.function(tree, self.funcdef)
            if tree.data == 'if_stmt':
                i = 0
                for ins in reversed(self.funcdef[-1]['instructions']):
                    if 'if_id' in ins:
                        ins['op_32'] = i
                        ins.pop('if_id')
                    if 'if_start' in ins and ins['if_start']:
                        ins['if_start'] = False
                        break
                    i += 1
            if tree.data == 'if_block_stmt':
                postfn.block_stmt(tree)
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'br', 'op_32': 0, 'if_id': self.__if_block})  # 跳出
                i = 0
                for ins in reversed(self.funcdef[-1]['instructions']):
                    if 'fill' in ins:
                        ins['op_32'] = i
                        ins.pop('fill')
                        break
                    i += 1
            if tree.data == 'while_block_stmt':
                postfn.block_stmt(tree)
                i = 0
                for ins in reversed(self.funcdef[-1]['instructions']):
                    if 'fill' in ins:
                        ins['op_32'] = i+1
                        ins.pop('fill')
                    if 'break' in ins and ins['break']:
                        ins['op_32'] = (i+1)
                        ins['break'] = False
                    if 'continue' in ins and ins['continue']:
                        ins['op_32'] = i
                        ins['continue'] = False
                    if 'while_start' in ins and ins['while_start']:
                        self.funcdef[-1]['instructions'].append(
                            {'ins': 'br', 'op_32': -(i+1)})
                        ins['while_start'] = False
                        break
                    i += 1
                self.__while_block -= 1
            if tree.data == 'break_stmt':
                if self.__while_block > 0:
                    self.funcdef[-1]['instructions'].append(
                        {'ins': 'br', 'op_32': 0, 'break': True})
                else:
                    raise RuntimeError('break must in a while block')
            if tree.data == 'continue_stmt':
                if self.__while_block > 0:
                    self.funcdef[-1]['instructions'].append(
                        {'ins': 'br', 'op_32': 0, 'continue': True})
                else:
                    raise RuntimeError('continue must in a while block')
            if tree.data == 'block_stmt':
                postfn.block_stmt(tree)
            if tree.data == 'let_decl_stmt':
                if len(tree.children) == 3:
                    if tree.children[1].data != tree.children[2].meta.empty:
                        raise RuntimeError('type check failed')
                    self.funcdef[-1]['instructions'].append(
                        {'ins': 'store.64'})
            if tree.data == 'const_decl_stmt':
                if tree.children[1].data != tree.children[2].meta.empty:
                        raise RuntimeError('type check failed')
                self.funcdef[-1]['instructions'].append({'ins': 'store.64'})
            if tree.data == 'return_stmt':
                postfn.return_stmt(tree, self.funcdef,self.globaldef)
            if tree.data == 'assign_expr':
                postfn.check_assign_type(tree)
                self.funcdef[-1]['instructions'].append({'ins': 'store.64'})
            if tree.data == 'call_expr':
                postfn.call_expr(tree, self.funcdef)
            if tree.data == 'as_expr':
                postfn.as_expr(tree,self.funcdef)
            if tree.data == 'equl':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.f'})
                self.funcdef[-1]['instructions'].append({'ins': 'not'})
            if tree.data == 'neq':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.f'})
            if tree.data == 'lt':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.f'})
                self.funcdef[-1]['instructions'].append({'ins': 'set.lt'})
            if tree.data == 'gt':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.f'})
                self.funcdef[-1]['instructions'].append({'ins': 'set.gt'})
            if tree.data == 'le':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.f'})
                self.funcdef[-1]['instructions'].append({'ins': 'set.gt'})
                self.funcdef[-1]['instructions'].append({'ins': 'not'})
            if tree.data == 'ge':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'cmp.f'})
                self.funcdef[-1]['instructions'].append({'ins': 'set.lt'})
                self.funcdef[-1]['instructions'].append({'ins': 'not'})
            if tree.data == 'add':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'add.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'add.f'})
            if tree.data == 'sub':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'sub.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'sub.f'})
            if tree.data == 'mul':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'mul.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'mul.f'})
            if tree.data == 'div':
                postfn.check_type(tree)
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'div.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'div.f'})
            if tree.data == 'neg':
                tree.meta.empty = tree.children[0].meta.empty
                if tree.meta.empty == 'int':
                    self.funcdef[-1]['instructions'].append({'ins': 'neg.i'})
                if tree.meta.empty == 'double':
                    self.funcdef[-1]['instructions'].append({'ins': 'neg.f'})
            if tree.data == 'float_num':
                tree.meta.empty = 'double' #用一个没用的字段存类型
            if tree.data == 'int_num':
                tree.meta.empty = 'int'
            if tree.data == 'char':
                tree.meta.empty = 'int'
            if tree.data == 'var':
                tree.meta.empty = postfn.get_type(tree)
        else:  # 叶节点
            if tree.type == 'INT':
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'push', 'op_64': int(tree.value)})
            if tree.type == 'CHAR':
                ch = eval(tree.value)
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'push', 'op_64': ord(ch)})
            if tree.type == 'IDENT':
                postfn.ident(tree, self.funcdef)
            if tree.type == 'FLOAT':
                self.funcdef[-1]['instructions'].append(
                    {'ins': 'push', 'op_64': float(tree.value)})
            if tree.type == "ESCAPED_STRING":
                postfn.str_exper(tree, self.funcdef, self.globaldef)
