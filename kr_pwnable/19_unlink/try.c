#include<stdio.h>
#include<stdlib.h>

typedef struct o{
	struct o* a;
	struct o* b;
	char s[8];
}OBJ;

int main(){
	OBJ* A = (OBJ*) malloc(sizeof(OBJ));
	printf("%x\n",&(A->a));
	printf("%x\n",&(A->b));
	printf("%x\n",A->s);
	return 0;
}
