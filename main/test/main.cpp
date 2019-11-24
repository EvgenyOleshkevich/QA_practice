#include <iostream>
#include <fstream>
#include <algorithm>

void Bubble(int* arr, int size)
{
	for (int i = size; i > 0; --i)
		for (int j = 1; j < i; ++j)
			if (arr[j] < arr[j - 1])
				std::swap(arr[j], arr[j - 1]);
}

void Insert(int* arr, int size)
{
	for (int i = 1; i < size; ++i)
	{
		int j = i;
		while (j > 0 && arr[j] < arr[j - 1])
		{
			std::swap(arr[j], arr[j - 1]);
			--j;
		}
	}
}

void MakeHeap(int arr[], int length)
{
	for (int i = 1; i < length; ++i)
	{
		//int j = i % 2 == 1 ? (i - 1) / 2 : (i - 2) / 2;
		int k = i;
		int j = (k - 1) / 2;

		while (j >= 0 && arr[j] < arr[k])
		{
			int t = arr[j];
			arr[j] = arr[k];
			arr[k] = t;
			k = j;
			j = (k - 1) / 2;
		}
	}
}

void SortHeap(int arr[], int length)
{
	for (int i = length - 1; i > 0; --i)
	{
		int t = arr[0];
		arr[0] = arr[i];
		arr[i] = t;

		int j = 0;
		int k = 1;
		while (k < i)
		{

			if (k + 1 < i)
			{
				if (arr[k + 1] > arr[k])
					++k;
				if (arr[j] > arr[k])
					break;
				t = arr[j];
				arr[j] = arr[k];
				arr[k] = t;
				j = k;
				k = (j << 1) + 1;
			}
			else if (arr[j] < arr[k])
			{
				t = arr[j];
				arr[j] = arr[k];
				arr[k] = t;
				j = k;
				k = (j << 1) + 1;
			}
			else
				break;
		}
	}
}



int main(int argc, const char* argv[])
{
	int type = std::atoi(argv[1]);
	setlocale(LC_ALL,"Rus");
	std::ifstream inFile(argv[2]);
	int size = 0;
	inFile >> size;
	auto arr = new int[size];
	for (int i = 0; i < size; ++i)
	{
		inFile >> arr[i];
	}
	inFile.close();
	switch(type)
	{
		case 1:
		{
			Bubble(arr, size);
		}
		case 2:
		{
			Insert(arr, size);
			break;
		}
		case 3:
		{
			MakeHeap(arr, size);
			SortHeap(arr, size);
			break;
		}
		case 4:
		{
			std::sort(arr, arr + size, [](int a, int b)
				{
					return a < b;
				});
			break;
		}
	}
	
	std::ofstream outFile(argv[3]);

	outFile << size << std::endl;
	for (int i = 0; i < size; ++i)
	{
		outFile << arr[i] << " ";
	}
	outFile.close();
	std::ofstream endFile(argv[4]);
	endFile << "ok";
	endFile.close();
	std::cout << "ok";
	return 0;
}