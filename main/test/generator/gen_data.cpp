#include <iostream>
#include <fstream>
#include <ctime>

int main(uint32_t argc, const char* argv[])
{
	size_t size = std::atoi(argv[1]);
	srand(time(0));
	std::ofstream outFile("test.txt");
	outFile << size << std::endl;
	for (size_t i = 0; i < size; ++i)
		outFile << rand() % 100 << " ";
	outFile.close();
	return 0;
}