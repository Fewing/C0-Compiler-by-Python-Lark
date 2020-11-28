from .table import ident_table
from lark import Tree

def program(tree :Tree):
    pass
def let_decl_stmt(tree :Tree):
    key = str(tree.children[1].data) + '-' + \
        str(tree.children[0].value)
    if key in ident_table[-1]:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        ident_table[-1][key] = 'var'


def const_decl_stmt(tree :Tree):
    key = str(tree.children[1].data) + '-' + \
        str(tree.children[0].value)
    if key in ident_table[-1]:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        ident_table[-1][key] = 'const'


def block_stmt(tree :Tree):
    ident_table.append({})


def function(tree :Tree):
    key = str('fnc'+'-'+tree.children[2].data) + '-' + \
        str(tree.children[0].value)
    if key in ident_table[-1]:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        ident_table[-1][key] = 'func'
