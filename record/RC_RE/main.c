#include "stdio.h"
int c[10];
int main()
{
	int a, b;
	scanf("%d %d", &a, &b);
	
	for (int i=-1000;i<=1000;i++)
		c[i] = i;
	printf("%d\n", a + b);
	return 0;
}