import struct


class C0ASM():

    __output = bytearray()

    __instructions = {
        'nop': 0x00,
        'push': 0x01,
        'pop': 0x02,
        'popn': 0x03,
        'dup': 0x04,
        'loca': 0x0a,
        'arga': 0x0b,
        'global': 0x0c,
        'load.8': 0x10,
        'load.16': 0x11,
        'load.32': 0x12,
        'load.64': 0x13,
        'store.8': 0x14,
        'store.16': 0x15,
        'store.32': 0x16,
        'store.64': 0x17,
        'alloc': 0x18,
        'free': 0x19,
        'stackalloc': 0x1a,
        'add.i': 0x20,
        'sub.i': 0x21,
        'mul.i': 0x22,
        'div.i': 0x23,
        'add.f': 0x24,
        'sub.f': 0x25,
        'mul.f': 0x26,
        'div.f': 0x27,
        'shl': 0x29,
        'slr': 0x2a,
        'and': 0x2b,
        'or': 0x2c,
        'xor': 0x2d,
        'not': 0x2e,
        'cmp.i': 0x30,
        'cmp.u': 0x31,
        'cmp.f': 0x32,
        'neg.i': 0x34,
        'neg.f': 0x35,
        'itof': 0x36,
        'ftoi': 0x37,
        'shrl': 0x38,
        'set.lt': 0x39,
        'set.gt': 0x3a,
        'br': 0x41,
        'br.false': 0x42,
        'br.true': 0x43,
        'call': 0x48,
        'ret': 0x49,
        'callname': 0x4a,
        'scan.i': 0x50,
        'scan.c': 0x51,
        'scan.f': 0x52,
        'print.i': 0x54,
        'print.c': 0x55,
        'print.f': 0x56,
        'print.s': 0x57,
        'println': 0x58,
        'panic': 0xfe,
    }

    def __init__(self, **kw):
        s = struct.Struct('> I I')
        self.__output += s.pack(0x72303b3e, 0x00000001)

    def asm_globaldef(self, value_list):
        s = struct.Struct('> I')
        self.__output += s.pack(len(value_list))
        for value in value_list:
            if value['type']=='int':
                s = struct.Struct('> B I q')
                self.__output += s.pack(value['is_const'], 8, value['value'])
            if value['type'] == 'string':
                s = struct.Struct('> B I')
                self.__output += s.pack(value['is_const'], len(value['value']))
                for ch in value['value']:
                    s = struct.Struct('> c')
                    self.__output += s.pack(ch)

    def asm_functiondef(self, func_list):
        s = struct.Struct('> I')
        self.__output += s.pack(len(func_list))
        for func in func_list:
            s = struct.Struct('> I I I I I')
            self.__output += s.pack(func['name'], func['return_slots'],
                                    func['param_slots'], func['loc_slots'], len(func['instructions']))
            for ins in func['instructions']:
                if 'op_32' in ins:
                    self.addop(ins['ins'], op_32=ins['op_32'])
                elif 'op_64' in ins:
                    self.addop(ins['ins'], op_32=ins['op_64'])
                else:
                    self.addop(ins['ins'])

    def addop(self, ins, op_32=None, op_64=None):
        ins = self.__instructions[ins]
        if op_32 != None:
            s = struct.Struct('> B i')
            self.__output += s.pack(ins, op_32)
        elif op_64 != None:
            s = struct.Struct('> B q')
            self.__output += s.pack(ins, op_64)
        else:
            s = struct.Struct('> B')
            self.__output += s.pack(ins)

    def get(self):
        return self.__output


if __name__ == "__main__":
    f = open('test.o', 'wb')
    asm = C0ASM()
    globaldef = [
        {'type': 'int', 'is_const': 0, 'value': 0},
        {'type': 'int', 'is_const': 1, 'value': 0},
    ]
    funcdef = [
        {'name': 1, 'return_slots': 0, 'param_slots': 0, 'loc_slots': 0,
            'instructions': [{'ins': 'push', 'op_64': 1},
                             {'ins': 'push', 'op_64': 2},
                             {'ins': 'add.i'},
                             {'ins': 'neg.i'}]},
    ]
    asm.globaldef(globaldef)
    asm.functiondef(funcdef)
    f.write(asm.get())
    f.close()
