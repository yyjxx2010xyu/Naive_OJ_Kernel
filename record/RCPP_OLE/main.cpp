#include <stdio.h>
#include <stdlib.h>

int main()
{
int a,b;

scanf("%d%d",&a,&b);
printf("%d\n",a+b);
for (int i=1;i<=10000000;i++)
	putchar('M');
return 0;
}