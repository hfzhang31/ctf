a = 0x21dd09ec
index = 0
def write(c):
    if(c>=31 and c <= 126):
        return True
    else:
        return False

def writable(c):
    if(c<0):
        c = ~(c+1)
    d = c//0x1000000
    e = (c//0x10000)%0x100
    f = (c//0x100)%0x100
    g = c%0x100
    if(write(d) and write(e) and write(f) and write(g)):
        return True
    else:
        return False
for i in range(ord('1'),ord('~')):
    for j in range(ord('1'),ord('~')):
        for k in range(ord('1'),ord('~')):
            for m in range(ord('1'),ord('~')):
                index = index+1
		if(index%100 == 0):
		    print hex(a-4*b)
                    print hex(b)
		b = i*0x1000000+j*0x10000+k*0x100+m
                if writable(a-4*b):
                    print hex(~(a-4*b+1))
                    print hex(b)
                    break
