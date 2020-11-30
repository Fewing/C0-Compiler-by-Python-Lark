from .table import ident_table
from lark import Tree


def program(tree: Tree):
    pass


def let_decl_stmt(tree: Tree, globaldef: list, fundef: list):
    key = str(tree.children[1].data) + '-' + \
        str(tree.children[0].value)
    if key in ident_table[-1]:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        if len(ident_table) == 1:  # 全局变量
            g_var = {}
            g_var['type'] = tree.children[1].data
            g_var['is_const'] = 0
            g_var['value'] = 0
            loc = len(globaldef)
            globaldef.append(g_var)
            ident_table[-1][key] = {
                'name': tree.children[0].value,
                'type': tree.children[1].data,
                'loc': loc,
                'para': False,
                'const': False,
                'global': True,
                'func': False,
            }
        else:  #局部变量
            loc = fundef[-1]['loc_slots']
            fundef[-1]['loc_slots'] += 1
            ident_table[-1][key] = {
                'name': tree.children[0].value,
                'type': tree.children[1].data,
                'loc': loc,
                'para': False,
                'const': False,
                'global': False,
                'func': False,
            }


def const_decl_stmt(tree: Tree, globaldef: list, fundef: list):
    key = str(tree.children[1].data) + '-' + \
        str(tree.children[0].value)
    if key in ident_table[-1]:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        if len(ident_table) == 1:  # 全局变量
            g_var = {}
            g_var['type'] = tree.children[1].data
            g_var['is_const'] = 1
            g_var['value'] = 0
            loc = len(globaldef)
            globaldef.append(g_var)
            ident_table[-1][key] = {
                'name': tree.children[0].value,
                'type': tree.children[1].data,
                'loc': loc,
                'para': False,
                'const': True,
                'global': True,
                'func': False,
            }
        else:  # 局部变量
            loc = fundef[-1]['loc_slots']
            fundef[-1]['loc_slots'] += 1
            ident_table[-1][key] = {
                'name': tree.children[0].value,
                'type': tree.children[1].data,
                'loc': loc,
                'para': False,
                'const': True,
                'global': False,
                'func': False,
            }


def block_stmt(tree: Tree):
    ident_table.append({})


def function(tree: Tree, fundef: list):
    if tree.children[1].data == 'function_param_list':
        ret_type = tree.children[2].data
    else:
        ret_type = tree.children[1].data
    key = str('fnc'+'-'+ret_type) + '-' + \
        str(tree.children[0].value)
    if key in ident_table[-1]:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        func = {}
        func['name'] = len(fundef)
        func['loc_slots'] = 0
        func['return_slots'] = 0
        func['param_slots'] = 0
        func['instructions'] = []
        if ret_type != 'void':
            func['return_slots'] = 1
        fundef.append(func)
        ident_table[0][key] = {
            'name': tree.children[0].value,
            'type': ret_type,
            'loc': func['name'],
            'const': True,
            'global': True,
            'func': True,
        }


def function_param(tree: Tree, fundef: list):
    func = fundef[-1]
    key = str(tree.children[1].data) + '-' + \
        str(tree.children[0].value)
    loc = func['param_slots']
    func['param_slots'] += 1
    ident_table[-1][key] = {
        'name': tree.children[0].value,
        'type': tree.children[1].data,
        'loc': loc,
        'para': True,
        'const': False,
        'global': False,
        'func': False,
    }
