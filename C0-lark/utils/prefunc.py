from .table import ident_table, func_table
from lark import Tree
from .stdlib import lib_table, lib_check_type


def program(tree: Tree):
    pass


def let_decl_stmt(tree: Tree, globaldef: list, funcdef: list):
    key = str(tree.children[0].value)
    if key in ident_table[-1]:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        if tree.children[1].data == 'void':
            raise RuntimeError('VoidTypeVariable: '+key)
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
            }
            if len(tree.children) == 3:
                funcdef[-1]['instructions'].append({
                    'ins': 'global',
                    'op_32': loc,
                })
        else:  # 局部变量
            loc = funcdef[-1]['loc_slots']
            funcdef[-1]['loc_slots'] += 1
            ident_table[-1][key] = {
                'name': tree.children[0].value,
                'type': tree.children[1].data,
                'loc': loc,
                'para': False,
                'const': False,
                'global': False,
            }
            if len(tree.children) == 3:
                funcdef[-1]['instructions'].append({
                    'ins': 'loca',
                    'op_32': loc,
                })
        tree.children[0].type = "ASSIIDENT"


def const_decl_stmt(tree: Tree, globaldef: list, funcdef: list):
    key = str(tree.children[0].value)
    if key in ident_table[-1]:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        if tree.children[1].data == 'void':
            raise RuntimeError('VoidTypeVariable: '+key)
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
            }
            funcdef[-1]['instructions'].append({
                'ins': 'global',
                'op_32': loc,
            })
        else:  # 局部变量
            loc = funcdef[-1]['loc_slots']
            funcdef[-1]['loc_slots'] += 1
            ident_table[-1][key] = {
                'name': tree.children[0].value,
                'type': tree.children[1].data,
                'loc': loc,
                'para': False,
                'const': True,
                'global': False,
            }
            funcdef[-1]['instructions'].append({
                'ins': 'loca',
                'op_32': loc,
            })
        tree.children[0].type = "ASSIIDENT"


def block_stmt(tree: Tree):
    ident_table.append({})


def function(tree: Tree, funcdef: list, globaldef: list):
    para_num = 0
    if tree.children[1].data == 'function_param_list':
        ret_type = tree.children[2].data
        para_num = len(tree.children[1].children)
    else:
        ret_type = tree.children[1].data
    key = str(tree.children[0].value)
    if key in func_table:
        raise RuntimeError('Duplicate declaration: '+key)
    else:
        g_var = {}
        g_var['type'] = 'string'
        g_var['is_const'] = 1
        g_var['value'] = key
        name = len(globaldef)
        globaldef.append(g_var)
        func = {}
        func['name'] = name
        func['loc_slots'] = 0
        func['return_slots'] = 0
        func['param_slots'] = 0
        func['instructions'] = []
        if ret_type != 'void':
            func['return_slots'] = 1
        funcdef.append(func)
        func_table[key] = {
            'name': tree.children[0].value,
            'type': ret_type,
            'loc': len(funcdef)-1,
            'para_num': para_num,
        }
    tree.children[0].type = "FNCIDENT"


def function_param(tree: Tree, funcdef: list):
    func = funcdef[-1]
    key = str(tree.children[0].value)
    loc = func['param_slots'] + func['return_slots']
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
    tree.children[0].type = "PARAIDENT"


def return_stmt(tree: Tree, funcdef: list):
    if funcdef[-1]['return_slots'] != 0:
        funcdef[-1]['instructions'].append({'ins': 'arga', 'op_32': 0})


def assign_expr(tree: Tree, funcdef: list):
    key = str(tree.children[0].value)
    for table in reversed(ident_table):
        if key in table:
            ident = table[key]
            tree.meta.empty = ident['type']
            if ident['const']:
                raise RuntimeError('can not assign const:' + key)
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
            tree.children[0].type = "ASSIIDENT"
            return
    raise RuntimeError('ident ' + key + ' is not declared')


def call_expr(tree: Tree, funcdef: list):
    key = str(tree.children[0].value)
    if key in func_table:
        tree.meta.empty = func_table[key]['type']
        func = func_table[key]
        if func['type'] != 'void':
            funcdef[-1]['instructions'].append({
                'ins': 'stackalloc',
                'op_32': 1,
            })
    elif key in lib_table:
        tree.meta.empty = lib_table[key]['type']
    else:
        raise RuntimeError('function ' + key + ' is not declared')
    tree.children[0].type = "FNCIDENT"
