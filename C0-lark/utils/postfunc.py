from .table import ident_table, func_table
from lark import Tree, Token
from .stdlib import lib_table, code_gen


def block_stmt(tree: Tree):
    ident_table.pop()


def return_stmt(tree: Tree, funcdef: list):
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
        raise RuntimeError(f'function {key} is not declared')


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
    raise RuntimeError(f'ident {token} is not declared')


def str_exper(token: Token, funcdef: list, globaldef: list):
    g_var = {}
    g_var['type'] = 'string'
    g_var['is_const'] = 1
    g_var['value'] = token.value[1:-1]
    loc = len(globaldef)
    globaldef.append(g_var)
    funcdef[-1]['instructions'].append({
        'ins': 'push',
        'op_32': loc,
    })
