#include <iostream>
#include <fstream>
#include <ctime>
#include <algorithm>

int main(int argc, const char* argv[])
{
	int size = std::atoi(argv[1]);
	srand(time(0));
	std::ofstream test(argv[2]);
	test << size << std::endl;
	int* arr = new int[size];
	for (int i = 0; i < size; ++i)
	{
		arr[i] = rand() % 1000;
		test << arr[i] << " ";
	}
	test.close();

	std::sort(arr, arr + size, [](int a, int b)
				{
					return a < b;
				});
	std::ofstream res(argv[3]);
	res << size << std::endl;
	for (int i = 0; i < size; ++i)
		res << arr[i] << " ";
	res.close();
	return 0;
}