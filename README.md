# Программа для сбора статистики при выполнении програм с различными параметрами и сбором статистики в многопроцессорных системах
[Техническое задание](https://docs.google.com/document/d/1JwbmkZAbK60ULANLYe0h7OMhNgVCNzGD975bmAHc-44/edit)
## Необходимые библиотеки для запуска
* numpy
* PyQt5
* matplotlib

## Как использовать программу
1. Склонировать репозиторий 
2. Открыть консоль и ввести "python пакеты.py"
3. В открывшемся окне ввести необходимые параметры запуска
4. Нажать кнопку calc
5. После окончания выполнения тестов будет выведено окно с статистикой тестов и графиком


### Параметры запуска:
* Path to executable scenario file - Путь до исполняемого файла (Обязателен)
* Path to file with test - путь до входных данных (или папки с входными данными) (Обязателен)
* Current Param Range - диапозон параметров для тестирования (Обязателен)
* Path to folder with default test results - Путь до папки с предпологаемыми результатами тестов (Необязательно)
* Path to folder to save the results - Путь до папки, куда сохранить результат текущего тестирования (Необязательно)
* Path to answers compatator exe file - Путь до файла - компаратора (Необязательно)
Формат путей должен быть следующим: "Какой то формат путей в linux"
