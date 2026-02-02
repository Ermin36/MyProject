## Проект "MyProject"

Проект "MyProject" был создан для обучения работы с python и его функциями

## Установка

1. Клонировать репозиторий

``git clone https://github.com/Ermin36/MyProject.git``

2. Подключить в своём проекте модуль scr\processing

``from utils.processing import *``
\- Импортирует все функции

## Использование

1. Функция ``filter_by_state(list_dict,state: str = "EXECUTED")``

Фильтрует список словарей по ключу 'state'

Пример:

```python
from utils.processing import filter_by_state

list_dict = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, 
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

new_list_dict = filter_by_state(list_dict)
```
Данный пример отсортирует список по 'state':"EXECUTED"

2. Функция ``sorted_by_date(list_dict, reverse = True)``

Сортирует список словарей по дате

Пример:

```python
from utils.processing import sort_by_date

list_dict = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, 
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

new_list_dict = sort_by_date(list_dict)
```
Отсортирует список по убыванию времени ключа 'date'

## Тесты

В папке `tests` есть модули для тестирования всех функций находящихся в папке `utils`
