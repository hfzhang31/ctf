/*
这题过滤了 / ，主要问题就是怎么获得到 /
可以切换到根目录，这样pwd 的输出结果就是 /
用$(pwd)来获得执行结果
然后在输入时加上一个单引号防止在filter时就已经替换成执行结果而被过滤
注意payload要写成 '"" ... ""'
这两个双引号是为了让system接受的参数仍然包含一对双引号
*/

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "=")!=0;
	r += strstr(cmd, "PATH")!=0;
	r += strstr(cmd, "export")!=0;
	r += strstr(cmd, "/")!=0;
	r += strstr(cmd, "`")!=0;
	r += strstr(cmd, "flag")!=0;
	return r;
}

extern char** environ;
void delete_env(){
	char** p;
	for(p=environ; *p; p++)	memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
	delete_env();
	putenv("PATH=/no_command_execution_until_you_become_a_hacker");
	if(filter(argv[1])) return 0;
	printf("%s\n", argv[1]);
	system( argv[1] );
	return 0;
}