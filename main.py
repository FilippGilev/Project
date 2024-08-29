import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import *

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def size(self):
        return len(self.items)

# Функция быстрой сортировки
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        start = arr[0] # Опорный элемент
        # Слева все элементы больше или равные опорному элементу
        left = [x for x in arr[1:] if x >= start]
        # Справа все элементы меньше опорного элемента
        right = [x for x in arr[1:] if x < start]
        return quick_sort(left) + [start] + quick_sort(right)


# Нахождение общей выручки
def total_revenue(data):
    total_costs = data['Общая стоимость'].values
    revenue = 0
    for cost in total_costs:
        revenue += cost
    return revenue

# Нахождение товара с наибольшим количеством продаж
def max_count(data):
    dict_count = {} # Создаем словарь
    for index, row in data.iterrows():
        name = row['Название'] # Ключ - название
        count = row['Количество'] # Значение - количество продаж
        if name in dict_count: # Если товар уже добавлен в словарь обновляем значение
            dict_count[name] += count
        else: # Если товара в словаре еще нет, добавляем его в словарь
            dict_count[name] = count
    total_count = [] # Создаем массив с количеством продаж каждого товара
    for key, value in dict_count.items():
        total_count.append(value) # Добавляем в массив значения из словаря
    sorted_total_count = quick_sort(total_count) # Используем быструю сортировку (по убыванию)
    max_count = sorted_total_count[0] # Максимальное количество продаж
    for key, value in dict_count.items():
        if value == max_count: # Находим товар, проданный больше всего раз
            return key, value, dict_count

# Построение гистограммы с названиями и их количеством продаж
def plot_count(dict_count):
    # Преобразование ключей и значений словаря в списки
    products = list(dict_count.keys())
    counts = list(dict_count.values())


    window = Tk()
    window.title('Продажи товаров')
    window.geometry('800x600')

    # Установка окна поверх всех других окон
    window.attributes('-topmost', 1)
    window.update_idletasks()

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(products, counts)
    ax.set_title('Продажи товаров')
    plt.xticks(rotation=45)
    ax.set_ylabel('Количество продаж')
    ax.set_yticks(range(0, max(counts) + max(counts) // 10, max(counts) // 10))
    ax.tick_params(labelsize=8)

    # Создание объекта для встроенной гистограммы Tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    # Размещение графика на окне Tkinter
    canvas.get_tk_widget().pack()

    window.mainloop()

def max_cost(data):
    dict_cost = {} # Создаем словарь
    for index, row in data.iterrows():
        name = row['Название'] # Ключ - название
        cost = row['Общая стоимость'] # Значение - общая стоимость
        if name in dict_cost:
            dict_cost[name] += cost # Если товар уже добавлен в словарь обновляем значение
        else: # Если товара в словаре еще нет, добавляем его в словарь
            dict_cost[name] = cost
    total_cost = [] # Создаем массив с общей стоимостью каждого товара
    for key, value in dict_cost.items():
        total_cost.append(value) # Добавляем в массив значения из словаря
    sorted_total_cost = quick_sort(total_cost) # Используем быструю сортировку (по убыванию)
    max_cost = sorted_total_cost[0] # Самый дорогой товар
    for key, value in dict_cost.items():
        if value == max_cost: # Находим название самого дорогого товара
            return key, value, dict_cost

# Построение гистограммы с названиями и их общей стоимостью
def plot_cost(dict_cost):
    # Преобразование ключей и значений словаря в списки
    products = list(dict_cost.keys())
    cost = list(dict_cost.values())

    window = Tk()
    window.title('Выручка с товаров')
    window.geometry('800x600')

    # Установка окна поверх всех других окон
    window.attributes('-topmost', 1)
    window.update_idletasks()

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.bar(products, cost)
    ax.set_title('Выручка с товаров')
    plt.xticks(rotation=45)
    ax.set_ylabel('Выручка')
    ax.set_yticks(range(0, max(cost) + max(cost) // 10, max(cost) // 10))
    ax.tick_params(labelsize=8)

    # Создание объекта для встроенной гистограммы Tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    # Размещение графика на окне Tkinter
    canvas.get_tk_widget().pack()

    window.mainloop()
def add_row(table, row_data, undo_stack):
    undo_stack.push(table.copy())  # Сохраняем предыдущее состояние таблицы
    new_row = pd.DataFrame([row_data], columns=table.columns)
    table = pd.concat([table, new_row], ignore_index=True)
    return table

def delete_row(table, row_data, undo_stack):
    # Преобразование списка row_data в строку для сравнения
    row_str = ','.join(map(str, row_data))
    # Проверяем, содержится ли строка в таблице
    if row_str in table.astype(str).agg(','.join, axis=1).values:
        undo_stack.push(table.copy())  # Сохраняем предыдущее состояние таблицы
        # Используем метод drop для удаления строки
        table = table[table.astype(str).agg(','.join, axis=1) != row_str]
        return table.reset_index(drop=True)  # Сбрасываем индексы
    else:
        print("Строка с такими данными не найдена.")
        return table  # Возвращаем исходную таблицу, если строка не найдена



try:
    data = pd.read_csv('data.csv')
    # Названия столбцов таблицы
    expected_columns = ['Номер', 'Дата', 'Название', 'Категория', 'Количество', 'Цена', 'Общая стоимость']
    missing_columns = set(expected_columns) - set(data.columns) # Находим названия пропущенных столбцов
    if missing_columns: # Если отсутствует столбец выводим ошибку
        raise ValueError(f"Отсутствуют необходимые столбцы - {', '.join(missing_columns)}")
except FileNotFoundError:
    print("Файл не найден.")
    exit()
except pd.errors.EmptyDataError:
    print("Ошибка: файл пустой.")
    exit()
except ValueError as ve:
    print(f"Ошибка: {ve}")
    exit()
# Непредвиденные ошибки
except Exception:
    print("Произошла ошибка при чтении файла")
    exit()
# Проверка формата данных в столбце "Номер"
if data['Номер'].dtype != 'int64':
    print("Ошибка: столбец 'Номер' содержит неправильный формат данных.")
    exit()
# Проверка формата данных в столбце "Дата"
try:
    pd.to_datetime(data['Дата'], format='%Y-%m-%d', errors='raise')
except ValueError:
    print("Ошибка: столбец 'Дата' содержит неправильный формат данных.")
    exit()
# Проверка формата данных в столбце "Название"
if not data['Название'].astype(str).str.isalpha().all() and not ' ':
    print("Ошибка: столбец 'Название' содержит неправильный формат данных.")
    exit()
# Проверка формата данных в столбце "Категория"
if not data['Категория'].astype(str).str.isalpha().all() and not ' ':
    print("Ошибка: столбец 'Категория' содержит неправильный формат данных.")
    exit()
# Проверка формата данных в столбце "Количество"
if data['Количество'].dtype != 'int64':
    print("Ошибка: столбец 'Количество' содержит неправильный формат данных.")
    exit()
# Проверка формата данных в столбце "Цена"
if data['Цена'].dtype != 'int64':
    print("Ошибка: столбец 'Цена' содержит неправильный формат данных.")
    exit()
# Проверка формата данных в столбце "Общая стоимость"
if data['Общая стоимость'].dtype != 'int64':
    print("Ошибка: столбец 'Общая стоимость' содержит неправильный формат данных.")
    exit()

# Считывания csv-файла и вывод таблицы по исходным данным
print(f"Таблица, проданных товаров в магазине:")
print(data.to_string(index=False))

undo_stack = Stack()

while True:
    print('\n1. Изменить данные в таблице\n2. Рассчитать общую выручку магазина\n'
    '3. Найти товар, проданный наибольшее количество раз\n4. Найти товар, принесший наибольшую выручку'
    '\n5. Составить отчет\n6. Завершить программу')
    try:
        action = int(input("Выберите действие: "))
        # Если не будет введено число от 1 до 6 выведется сообщение
        if action not in range(1, 7):
            raise ValueError
    except ValueError:
        print("\nПожалуйста, введите число от 1 до 6.\n")
        continue
    match action:
        case 1:
            print('\n1. Добавить данные в таблицу\n2. Удалить данные из таблицы\n3. Отменить последнюю операцию\n')
            try:
                sub_action = int(input("Выберите действие: "))
                if sub_action not in range(1, 4):
                    raise ValueError
            except ValueError:
                print("\nПожалуйста, введите число от 1 до 3.\n")
                continue
            match sub_action:
                case 1:
                    try:
                        row_data = input("\nВведите данные для новой строки (Номер,Дата,Название,Категория,"
                        "Количество,Цена,Общая стоимость):\n")
                        row_data = row_data.split(",")
                        if len(row_data) != 7:
                            raise ValueError("Неверное количество данных для добавления строки.")
                        row_data = [int(row_data[0]), str(row_data[1]), str(row_data[2]), str(row_data[3]),
                                    int(row_data[4]), int(row_data[5]), int(row_data[6])]
                        data = add_row(data, row_data, undo_stack)
                        print(data.to_string(index=False))
                    except ValueError as ve:
                        print(f"Ошибка: {ve}")
                case 2:
                    row_data = input("\nВведите данные строки для удаления (Номер,Дата,Название,Категория,"
                    "Количество,Цена,Общая стоимость):\n")
                    row_data = row_data.split(",")
                    data = delete_row(data, row_data, undo_stack)
                    print(data.to_string(index=False))
                case 3:
                    if not undo_stack.is_empty():
                        table = undo_stack.pop()  # Восстанавливаем предыдущее состояние таблицы
                        print(table.to_string(index=False))
                    else:
                        print("\nНет действий для отмены.")
        case 2:
            # Подсчет общей выручки
            print(f'\nОбщая выручка магазина составляет {total_revenue(data)} рублей\n')
        case 3:
            # Нахождение товара с наибольшим количеством продаж
            name, count, dict_count = max_count(data)
            print(f'\nТовар "{name}" был продан наибольшее количество раз - {count}\n')
            plot_count(dict_count)
        case 4:
            # Нахождение товара с наибольшей стоимостью
            name, cost, dict_cost = max_cost(data)
            print(f'\nТовар "{name}" принес наибольшую выручку - {cost} рублей\n')
            plot_cost(dict_cost)
        case 5:
            # Составление итогового отчета
            report = data.groupby('Название').agg({
                'Категория': 'first',
                'Количество': 'sum',
                'Цена': 'first',
                'Общая стоимость': 'sum',
            }).reset_index()

            # Отчет будет иметь столбцы Название, Категория, Количество, Цена, Общая стоимость, Доля общей выручки
            df = pd.DataFrame(report)
            df['Доля от общей выручки, %'] = round(df['Общая стоимость'] / total_revenue(data) * 100, 2)
            print(f'\nИтоговый отчет: общая выручка магазина - {total_revenue(data)} рублей')
            print(df.to_string(index=False) + '\n')
        case 6:
            # Завершение программы
            print("\nПрограмма завершена")
            exit()