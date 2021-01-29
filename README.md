# C0-Compiler-by-Python-Lark

BUAA软件学院2018级编译原理与技术C0大作业，基于[python-lark](https://github.com/lark-parser/lark)解析器实现。

语法参考：https://c0.karenia.cc/ 已实现所有扩展
## 使用

* C0源文件编译为二进制文件
```
python3 C0-lark/main.py C0-lark/test.c0 -o C0-lark/test.o0
```

* 使用[虚拟机](https://github.com/BUAA-SE-Compiling/natrium/releases)运行二进制文件
```
navm.exe test.o0
```
