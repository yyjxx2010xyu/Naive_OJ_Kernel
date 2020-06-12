#include <iostream>

using namespace std;

int c[10];
int main()
{
	int a, b;
	cin >> a >> b;
	for (int i=-1000;i<=1000;i++)
		c[i] = i;
	cout << a + b << endl;
	return 0;
}