#include <stdio.h>

int main()
{
	int a, b;
	for (int i=1;i<=100000;i++)
	{
		int* c = (int *) malloc(sizeof(int) * 1000000);
		for (int j=1;j<1000000;j++)
			c[j] = j;
	}
	scanf("%d %d", &a, &b);
	printf("%d\n", a + b);
	return 0;
}