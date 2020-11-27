from lark import Lark
import sys

if __name__ == "__main__":
    input_path = sys.argv[1]
    input_file = open(input_path)
    input_str = input_file.read()

    output_path = sys.argv[3]
    ouput_file = open(output_path,'w')

    lark_file = open('C0-lark/C0.lark')
    lark_str = lark_file.read()
    lark = Lark(lark_str)

    res = lark.parse(input_str)
    ouput_file.write(res.pretty())

    input_file.close()
    ouput_file.close()