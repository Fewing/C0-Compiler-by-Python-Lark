from .table import ident_table, func_table
from lark import Tree, Token
from .stdlib import lib_table, code_gen


def function(tree: Tree, funcdef: list):
    key = str(tree.children[0].value)
    if func_table[key]['type'] == 'void' and (len(funcdef[-1]['instructions']) == 0 or funcdef[-1]['instructions'][-1] != {'ins': 'ret'}):
        funcdef[-1]['instructions'].append({'ins': 'ret'})
    else:
        if funcdef[-1]['instructions'][-1] != {'ins': 'ret'}:
            raise RuntimeError('Not All Routes Return')


def block_stmt(tree: Tree):
    ident_table.pop()


def return_stmt(tree: Tree, funcdef: list, globaldef: list):
    ret_type = func_table[globaldef[funcdef[-1]['name']]['value']]['type']
    if len(tree.children) == 1:
        if tree.children[0].meta.empty != ret_type:
            raise RuntimeError('type check failed, need')
    elif ret_type != 'void':
        raise RuntimeError('type check failed, need')
    if funcdef[-1]['return_slots'] != 0:
        funcdef[-1]['instructions'].append({'ins': 'store.64'})
    funcdef[-1]['instructions'].append({'ins': 'ret'})


def call_expr(tree: Tree, funcdef: list):
    key = str(tree.children[0].value)
    if key in func_table:
        loc = func_table[key]['loc']
        funcdef[-1]['instructions'].append({'ins': 'call', 'op_32': loc})
    elif key in lib_table:
        code_gen(key, funcdef)
    else:
        raise RuntimeError('function ' + key + ' is not declared')


def ident(token: Token, funcdef: list):
    for table in reversed(ident_table):
        if token in table:
            ident = table[token]
            if ident['para']:
                funcdef[-1]['instructions'].append({
                    'ins': 'arga',
                    'op_32': ident['loc'],
                })
            elif ident['global']:
                funcdef[-1]['instructions'].append({
                    'ins': 'global',
                    'op_32': ident['loc'],
                })
            else:
                funcdef[-1]['instructions'].append({
                    'ins': 'loca',
                    'op_32': ident['loc'],
                })
            funcdef[-1]['instructions'].append({
                'ins': 'load.64',
            })
            return
    raise RuntimeError('ident ' + token + ' is not declared')


def str_exper(token: Token, funcdef: list, globaldef: list):
    g_var = {}
    g_var['type'] = 'string'
    g_var['is_const'] = 1
    g_var['value'] = eval(token.value)
    loc = len(globaldef)
    globaldef.append(g_var)
    funcdef[-1]['instructions'].append({
        'ins': 'push',
        'op_64': loc,
    })


def as_expr(tree: Tree, funcdef: list):
    tree.meta.empty = tree.children[1].data
    if tree.children[0].meta.empty == 'double' and tree.meta.empty == 'int':
        funcdef[-1]['instructions'].append({'ins': 'ftoi', })
    if tree.children[0].meta.empty == 'int' and tree.meta.empty == 'double':
        funcdef[-1]['instructions'].append({'ins': 'itof', })


def check_type(tree: Tree):
    if tree.children[0].meta.empty != tree.children[1].meta.empty:
        raise RuntimeError('type check failed')
    tree.meta.empty = tree.children[0].meta.empty


def check_assign_type(tree: Tree):
    if tree.meta.empty != tree.children[1].meta.empty:
        raise RuntimeError('type check failed')


def get_type(tree: Tree):
    key = tree.children[0]
    for table in reversed(ident_table):
        if key in table:
            return table[key]['type']
    return 'void'
