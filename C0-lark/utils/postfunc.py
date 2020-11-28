from .table import ident_table
from lark import Tree

def block_stmt(tree :Tree):
    ident_table.pop()