#include <iostream>
#include <fstream>
#include <ctime>

int main()
{
	srand(time(0));
	size_t size = 0;
	std::cin >> size;
	std::ofstream outFile("test.txt");
	outFile << size << std::endl;
	for (size_t i = 0; i < size; ++i)
		outFile << rand() % 100 << " ";
	outFile.close();
	return 0;
}