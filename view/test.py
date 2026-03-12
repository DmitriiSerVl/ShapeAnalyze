class MyClass:
    def __init__(self, *args):
        # args — это кортеж, содержащий все переданные аргументы
        self.items = args

# Создание объекта с разным количеством аргументов
obj1 = MyClass(1, 2, 3)
print(obj1.items[2])  # Вывод: (1, 2, 3)

obj2 = MyClass("a", "b")
print(obj2.items)  # Вывод: ('a', 'b')
