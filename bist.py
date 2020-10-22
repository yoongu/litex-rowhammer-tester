#!/usr/bin/env python3

from litex import RemoteClient
import time

wb = RemoteClient()
wb.open()

# --------------------------------------------------------------------

wb.regs.writer_start.write(0)
wb.regs.writer_reset.write(1)
time.sleep(10000 / 1e6)
wb.regs.writer_reset.write(0)

wb.write(0x20000000, 0xffffffff) # patttern
wb.write(0x21000000, 0xffffffff) # patttern
wb.write(0x22000000, 0xffffffff) # patttern
wb.write(0x23000000, 0xffffffff) # patttern
wb.write(0x24000000, 0x00000000) # offset

mem_range = 256 * 1024 * 1024 # bytes
mem_mask  = (mem_range // 4 // 4) - 1
mem_count = mem_mask

wb.regs.writer_mem_mask.write(mem_mask) # memory range
wb.regs.writer_data_mask.write(0x00000000) # just pattern from address 0x0
wb.regs.writer_count.write(mem_count)
wb.regs.writer_start.write(1)

while True:
    if wb.regs.writer_done.read():
        break
    else:
        time.sleep(10000 / 1e6)

wb.regs.writer_start.write(0)


#print('bist: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 0 * 4, 16)]))
#print('bist: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 4 * 4 * 4, 16)]))
#print('bist: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 8 * 4 * 4, 16)]))
#print('bist: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 12 * 4 * 4, 16)]))

# FIXME: random
off = 67108864 - 100
wb.write(0x40000000 + off * 4, 0xffffefff)

#print('bist: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 0 * 4, 16)]))
#print('bist: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 4 * 4 * 4, 16)]))
#print('bist: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 8 * 4 * 4, 16)]))
#print('bist: ' + str(["0x{:08x}".format(w) for w in wb.read(0x40000000 + 12 * 4 * 4, 16)]))

wb.regs.reader_start.write(0)
wb.regs.reader_reset.write(1)
time.sleep(10000 / 1e6)
wb.regs.reader_reset.write(0)

# Expected pattern
wb.write(0x30000000, 0xffffffff) # patttern
wb.write(0x31000000, 0xffffffff) # patttern
wb.write(0x32000000, 0xffffffff) # patttern
wb.write(0x33000000, 0xffffffff) # patttern
wb.write(0x34000000, 0x00000000) # offset

wb.regs.reader_mem_mask.write(mem_mask) # memory range
wb.regs.reader_data_mask.write(0x00000000) # pattern range
wb.regs.reader_count.write(mem_count)
wb.regs.reader_start.write(1)
wb.regs.reader_start.write(0)

while True:
    if wb.regs.reader_done.read():
        break
    else:
        time.sleep(1000 / 1e6)

# FIXME: assert
print('ptr: 0x{:08x}'.format(wb.regs.reader_pointer.read()))

wb.close()
