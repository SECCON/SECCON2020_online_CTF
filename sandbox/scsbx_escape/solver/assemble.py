import sys
import struct

cpuset = {
    # memory
    'pop': b'\x21', 'dup': b'\x22', 'xchg': b'\x23',
    'load32': b'\x24', 'load64': b'\x25', 'show': b'\x70',
    'store8': b'\x26', 'store16': b'\x27', 'store32': b'\x28',
    # branch
    'jmp': b'\x30', 'jeq': b'\x31', 'jgt': b'\x32', 'jge': b'\x33',
    'call': b'\x34',
    # arith
    'add': b'\x40', 'sub': b'\x41', 'mul': b'\x42', 'div': b'\x43',
    'mod': b'\x44', 'abs': b'\x45', 'neg': b'\x46',
    # logic
    'not': b'\x50', 'and': b'\x51', 'or': b'\x52', 'xor': b'\x53',
    'shl': b'\x54', 'shr': b'\x55',
    # system
    'sys_read': b'\x60', 'sys_write': b'\x61',
    'sys_map': b'\x62', 'sys_unmap': b'\x63',
    'sys_exit': b'\x64'
}

def assemble(asm):
    code = b''
    labels = {}

    # find all labels
    cur = 0
    for line in asm.split('\n'):
        instr = line.strip().split(' ')
        if instr == ['']: continue

        if instr[0][-1] == ':':
            labels[instr[0][:-1]] = cur
            continue

        op = instr[0].lower()
        if op == 'push':
            cur += 5
        elif op in cpuset:
            cur += 1

    # assemble
    for line in asm.split('\n'):
        instr = line.strip().split(' ')
        if instr == ['']: continue

        # skip comment and label
        if instr[0][0] == ';' or instr[0][-1] == ':':
            continue

        # instructions
        op = instr[0].lower()
        if op == 'push':
            try:
                value = int(instr[1], 16) if instr[1].startswith('0x') else int(instr[1])
            except:
                value = labels[instr[1]]
            code += b'\x20' + struct.pack('<I', value)
        else:
            code += cpuset[op]

    return code

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
    else :
        filepath = "challenge.S"
    with open(filepath, "r") as f:
        code = assemble(f.read())
    print("[+] Assemble Success!")
    with open("output.bin", "wb") as f:
        f.write(code)
