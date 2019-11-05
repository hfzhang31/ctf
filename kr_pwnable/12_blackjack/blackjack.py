#coding = utf-8
from pwn import *
import re

r = remote('pwnable.kr',9009)
print(r.recv())
r.sendline("y")
print(r.recv())
r.sendline("1")
init_str = r.recv()
p = re.compile(r'\d+')
data = p.findall(init_str)
card = int(data[0])
my = int(data[1])
his = int(data[2])

print(init_str)
r.sendline("100")
print(r.recv())




#print num,'[+]',chance
for i in range(0,100):
    print '[*]','='*18," ",i," ","="*18 ,"[*]"
    recvword = r.recvline()
    print "[+]server: ",recvword
    p = re.compile(r'\d+')
    data = p.findall(recvword)
    num = int(data[0])
    chance = int(data[1])
    choose_coin(num,chance,r)
print r.recv()