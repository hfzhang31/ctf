#include <stdio.h>
int main(){
        setresuid(getegid(), getegid(), getegid());
        setresgid(getegid(), getegid(), getegid());
        system("/home/shellshock/bash -c 'echo shock_me'");
        return 0;
}

//暂时没弄懂是什么操作
//https://www.freebuf.com/articles/system/45390.html
//https://www.cnblogs.com/p4nda/p/7119218.html