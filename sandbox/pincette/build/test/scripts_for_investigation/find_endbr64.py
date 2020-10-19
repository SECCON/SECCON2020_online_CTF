#!/usr/bin/env python
import sys
buf = open(sys.argv[1]).read()
start = 0
while True:
    rslt = buf.find("f30f1efa", start)
    if rslt == -1:
        break
    print "0x%x" % rslt
    start = rslt + 1
