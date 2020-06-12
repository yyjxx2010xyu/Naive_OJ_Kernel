#include <iostream>

using namespace std;

int main()
{
	int a, b;
	if (1)
	{
		goto start;
	}
start:
	cin >> a >> b;
	cout << a + b << endl;
	return 0;
}