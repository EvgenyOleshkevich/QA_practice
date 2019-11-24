#include <iostream>
#include <ctime>

int main(int argc, const char* argv[])
{
    srand(time(0));
    std::cout << (rand() % 2 == 0);
    return 0;
}