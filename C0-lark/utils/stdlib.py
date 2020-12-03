from .table import ident_table, func_table
from lark import Tree

lib_table = {
    'getint': {
        'para_num': 0,
        'type': 'int',
    },
    'getdouble': {
        'para_num': 0,
        'type': 'double',
    },
    'getchar': {
        'para_num': 0,
        'type': 'int',
    },
    'putint': {
        'para_num': 1,
        'type': 'void',
    },
    'putdouble': {
        'para_num': 1,
        'type': 'void',
    },
    'putchar': {
        'para_num': 1,
        'type': 'void',
    },
    'putstr': {
        'para_num': 1,
        'type': 'void',
    },
    'putln': {
        'para_num': 0,
        'type': 'void',
    },
}


def lib_check_type(name: str,):
    if name == 'getint':
        pass
    if name == 'getdouble':
        pass
    if name == 'getchar':
        pass
    if name == 'putint':
        pass
    if name == 'putdouble':
        pass
    if name == 'putchar':
        pass
    if name == 'putstr':
        pass
    if name == 'putln':
        pass


def code_gen(name: str, fundef: list):
    if name == 'getint':
        fundef[-1]['instructions'].append({
            'ins': 'scan.i',
        })
    if name == 'getdouble':
        fundef[-1]['instructions'].append({
            'ins': 'scan.f',
        })
    if name == 'getchar':
        fundef[-1]['instructions'].append({
            'ins': 'scan.c',
        })
    if name == 'putint':
        fundef[-1]['instructions'].append({
            'ins': 'print.i',
        })
    if name == 'putdouble':
        fundef[-1]['instructions'].append({
            'ins': 'print.f',
        })
    if name == 'putchar':
        fundef[-1]['instructions'].append({
            'ins': 'print.c',
        })
    if name == 'putstr':
        fundef[-1]['instructions'].append({
            'ins': 'print.s',
        })
    if name == 'putln':
        fundef[-1]['instructions'].append({
            'ins': 'println',
        })
