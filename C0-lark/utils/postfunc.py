from .table import ident_table, func_table
from lark import Tree, Token
from .stdlib import lib_table, code_gen


def block_stmt(tree: Tree):
    ident_table.pop()


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
