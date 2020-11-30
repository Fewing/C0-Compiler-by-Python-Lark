from .table import ident_table, func_table
from lark import Tree

lib_table = {
    'getint': {
        'para_num': 0,
    },
    'getdouble': {
        'para_num': 0,
    },
    'getchar': {
        'para_num': 0,
    },
    'putint': {
        'para_num': 1,
    },
    'putdouble': {
        'para_num': 1,
    },
    'putchar': {
        'para_num': 1,
    },
    'putstr': {
        'para_num': 1,
    },
    'putln': {
        'para_num': 0,
    },
}


def add_ret(name: str, fundef: list):
    fundef[-1]['instructions'].append({
        'ins': 'stackalloc',
        'op_32': lib_table[name]['para_num'],
    })


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
