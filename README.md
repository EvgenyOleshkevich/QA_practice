# QA PRACTICE
## Программа для сбора статистики при выполнении программ с различными параметрами в многопроцессорных системах
[Техническое задание](https://docs.google.com/document/d/1JwbmkZAbK60ULANLYe0h7OMhNgVCNzGD975bmAHc-44/edit)
## Язык разработки - Python 3.7
## Необходимые библиотеки для работы программы
* numpy
* PyQt5
* matplotlib

## Как использовать программу
1. Склонировать репозиторий 
2. Открыть консоль и ввести "python пакеты.py"
3. В открывшемся окне ввести необходимые параметры запуска
4. Нажать кнопку calc
5. После окончания выполнения тестов будет выведено окно со статистикой тестов и графиком
### Необязательные поля для ввода:
* Если пользователь не заполнил пункт 5, то программа сама сохранит результаты тестов в определенном формате в папке сохраненного репозитория
* Если пользователь не заполнил пункты 4/6, то тогда программа не будет проверять корректность посчитанных значений


### Параметры запуска:
1. Path to executable scenario file - Путь до исполняемого файла (Обязателен)
2. Path to file with test - путь до входных данных (или папки с входными данными) (Обязателен)
3. Current Param Range - диапозон параметров для тестирования (Обязателен) 
(Минимальное значение параметра: 1, максимальное: 1000)
4. Path to folder with default test results - Путь до папки с предпологаемыми результатами тестов (Необязательно)
5. Path to folder to save the results - Путь до папки, куда сохранить результат текущего тестирования (Необязательно)
6. Path to answers compatator exe file - Путь до файла - компаратора (Необязательно)

Формат путей должен быть следующим: "Какой то формат Абсолютного пути в linux"
