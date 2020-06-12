#include <iostream>

using namespace std;

int main()
{
	int a, b;
	cin >> a >> b;
	for (int i=1;i<=100000;i++)
	{
		int* c = new int[1000000];
		for (int j=1;j<1000000;j++)
			c[j] = j;
	}
	cout << a + b << endl;
	return 0;
}