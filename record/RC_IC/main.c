#include <stdio.h>

int main()
{
	int a, b;
	if (1)
	{
		goto start;
	}
start:
	scanf("%d %d", &a, &b);
	printf("%d\n", a + b);
	return 0;
}