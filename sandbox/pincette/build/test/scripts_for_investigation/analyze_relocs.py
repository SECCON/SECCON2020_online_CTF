#!/usr/bin/env python
import sys
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.elf.descriptions import describe_reloc_type
from IPython import embed
from struct import unpack
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)

"""
F3 0F 1E FA   for ENDBR64

<pattern>
0F 1E FA 00 00 00 00 00
F3 0F 1E FA 00 00 00 00
?? F3 0F 1E FA 00 00 00
00 00 F3 0F 1E FA 00 00 <- NG (kernel memory)

imm + 0xXXXXXXXXXXXXX000 = 0xFA1E0F
imm + 0xXXXXXXXXXXXXX000 = 0xFA1E0FF3
imm + 0xXXXXXXXXXXXXX000 = 0xFA1E0FF3YY
"""
GADGET_SIZE=128

def process_file(fname):
    with open(fname, 'rb') as f:
        e = ELFFile(f)
        # search for code segment
        for seg in e.iter_segments():
            if seg.header['p_flags'] == 5:
                code_start = seg.header['p_offset']
                code_end = code_start + seg.header['p_memsz'] - 1
                break
        for section in e.iter_sections():
            if not isinstance(section, RelocationSection):
                continue
            print "%s with %d relocations:" % (section.name, section.num_relocations())
            for relocation in section.iter_relocations():
                r_offset = relocation['r_offset']
                if relocation['r_info_type'] == 8:
                    if r_offset >= code_start and r_offset <= code_end:
                        offset_in_seg = r_offset - code_start
                        imm = unpack("Q", seg.data()[offset_in_seg:offset_in_seg+8])[0]
                        text = ""
                        if (imm & 0xfff) == 0x0ff3:
                            text += "baseaddr: 0x%x\n" % (0xfa1e0ff3 - imm)
                            baseaddr = (0xfa1e0ff3 - imm)
                            ibytes = seg.data()[offset_in_seg+4:offset_in_seg+4+GADGET_SIZE]
                            istart = baseaddr + code_start + offset_in_seg + 4
                        elif (imm & 0xf00 == 0x300):
                            text += "baseaddr: 0x%x\n" % ((0xfa1e0ff3ff - imm)&0xffffffffffffff00)
                            baseaddr = ((0xfa1e0ff3ff - imm)&0xffffffffffffff00)
                            ibytes = seg.data()[offset_in_seg+5:offset_in_seg+5+GADGET_SIZE]
                            istart = baseaddr + code_start + offset_in_seg + 5
                        elif (imm & 0xfff) == 0xe0f and seg.data()[offset_in_seg-1] == '\xf3':
                            text += "baseaddr: 0x%x\n" % (0xfa1e0f - imm)
                            baseaddr = (0xfa1e0f - imm)
                            ibytes = seg.data()[offset_in_seg+3:offset_in_seg+3+GADGET_SIZE]
                            istart = baseaddr + code_start + offset_in_seg + 3
                        else:
                            continue
                        found = False
                        for insn in md.disasm(ibytes, istart):
                            text += "0x%x:\t%20s\t%s\t%s\n" %(insn.address, str(insn.bytes).encode("hex"), insn.mnemonic, insn.op_str)
                            if insn.mnemonic == "ret":
                                found = True
                                break
                            """
                            if insn.mnemonic.startswith("j"):
                                break
                            """
                        if found:
                            print text

                        #embed()
                        #sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        process_file(sys.argv[1])
