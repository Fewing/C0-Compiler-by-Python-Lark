from lark import Lark

f_lark = open('test.lark')
lark = f_lark.read()
l = Lark(lark)
res = l.parse('''
if x > 0 {
  x = x + 1;
}
''')
print(res.pretty())
