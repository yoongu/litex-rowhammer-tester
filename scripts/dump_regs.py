#!/usr/bin/env python3

import sys
from litex import RemoteClient

if '--srv' in sys.argv[1:]:
    from wrapper import litex_srv
    litex_srv()

wb = RemoteClient()
wb.open()

#wb.regs.ctrl_reset.write(1)

# Dump all CSR registers of the SoC
for name, reg in wb.regs.__dict__.items():
    print("0x{:08x} : 0x{:08x} {}".format(reg.addr, reg.read(), name))

wb.close()
