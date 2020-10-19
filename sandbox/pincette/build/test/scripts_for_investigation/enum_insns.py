#!/usr/bin/env python
import sys
from IPython import embed
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)

template = "000000f30f1000f30f5945ccf30f58c15dc3".decode("hex")
for i in range(0x80):
    ibytes = chr(i) + template[1:]
    print "[i = 0x%02x]" % i
    for insn in md.disasm(ibytes, 0):
        print "%s %s" % (insn.mnemonic, insn.op_str)
        #embed()
        #sys.exit(0)
        #print insn
    print

