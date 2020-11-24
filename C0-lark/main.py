from lark import Lark

f_lark = open('test.lark')
lark = f_lark.read()
l = Lark(lark)
res = l.parse(" a + 1 * ( 4 + 2 ) >= -1 + 2 * a + 4")
print(res.pretty())
