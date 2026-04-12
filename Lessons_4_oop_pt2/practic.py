"""
1. Створіть базовий клас Engine, який буде відповідати за керування двигуном:
Метод start_engine() повинен виводити повідомлення "Engine started".
Метод stop_engine() повинен виводити повідомлення "Engine stopped".

Створіть базовий клас Vehicle, який буде містити загальні властивості та методи для транспорту:
Атрибут max_speed для зберігання максимальної швидкості.
Метод drive() повинен виводити повідомлення "Driving at maximum speed of {max_speed}".

Реалізуйте клас Car, який наслідує функціонал від Engine і Vehicle:
Додайте атрибут model для зберігання назви моделі машини.
Перевизначте метод drive() так, щоб він виводив повідомлення "Car {model} is driving at {max_speed}".

Реалізуйте клас Boat, який також наслідує Engine і Vehicle:
Додайте атрибут type для зберігання типу човна (наприклад, моторний, вітрильний).
Перевизначте метод drive() так, щоб він виводив повідомлення "Boat of type {type} is sailing at {max_speed}".

Створіть клас AmphibiousVehicle, який наслідує Car і Boat:
Метод drive() повинен перевіряти, якщо транспортний засіб знаходиться на суші — виводити повідомлення для машини, а якщо на воді — для човна.
Використовуйте атрибут is_on_land для визначення поточного стану.
"""


class Engine:
    def start_engine(self):
        print("Engine started")

    def stop_engine(self):
        print("Engine stopped")


class Vehicle:
    def __init__(self, max_speed):
        self.max_speed = max_speed

    def drive(self):
        print(f"Driving at maximum speed of {self.max_speed}")


class Car(Engine, Vehicle):
    def __init__(self, model, max_speed):
        Vehicle.__init__(self, max_speed)
        self.model = model

    def drive(self):
        print(f"Car {self.model} is driving at {self.max_speed}")


class Boat(Engine, Vehicle):
    def __init__(self, type, max_speed):
        Vehicle.__init__(self, max_speed)
        self.type = type

    def drive(self):
        print(f"Boat of type {self.type} is sailing at {self.max_speed}")


class AmphibiousVehicle(Car, Boat):
    def __init__(self, model, type, max_speed, is_on_land):
        Car.__init__(self, model, max_speed)
        Boat.__init__(self, type, max_speed)
        self.is_on_land = is_on_land

    def drive(self):
        if self.is_on_land:
            Car.drive(self)
        else:
            Boat.drive(self)


print("--- Task 1: AmphibiousVehicle ---")
av = AmphibiousVehicle("AmphiCar", "motor", 120, True)
av.start_engine()
av.drive()
av.is_on_land = False
av.drive()
av.stop_engine()

"""
2. Створіть клас Library, який буде представляти бібліотеку. Бібліотека повинна містити список книг. Для роботи з об’єктами цього класу реалізуйте перевантаження операторів.
   Для книги також створіть клас, перевантажте рядкове представлення (str). Для книги реалізуйте оператори порівняння за кількістю сторінок.
   Реалізуйте property для полів книги.

У бібліотеці необхідно реалізувати такі методи:
- додавання книги в бібліотеку — має бути метод і оператор +=, який додає книгу
- видалення книги — метод і оператор -=
- перевірка, чи міститься книга в бібліотеці — оператор in
- перевантажити len, який буде повертати кількість книг у бібліотеці
"""


class Book:
    def __init__(self, title, author, pages):
        self._title = title
        self._author = author
        self._pages = pages

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def pages(self):
        return self._pages

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.pages == other.pages
        return False

    def __lt__(self, other):
        if isinstance(other, Book):
            return self.pages < other.pages
        return NotImplemented


class Library:
    def __init__(self):
        self._books = []

    def add_book(self, book):
        self._books.append(book)

    def remove_book(self, book):
        self._books.remove(book)

    def __iadd__(self, book):
        self.add_book(book)
        return self

    def __isub__(self, book):
        self.remove_book(book)
        return self

    def __contains__(self, book):
        return book in self._books

    def __len__(self):
        return len(self._books)

print("\n--- Task 2: Library and Book ---")
library = Library()
book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", 180)
book2 = Book("To Kill a Mockingbird", "Harper Lee", 281)
print(book1)
print(book2)
print("book1 < book2 (by pages):", book1 < book2)
library += book1
library += book2
print("len(library):", len(library))
print("book1 in library:", book1 in library)
library -= book1
print("after removing book1, len(library):", len(library))
print("book1 in library:", book1 in library)

"""
3. Напишіть клас-декоратор, який кешує результати методів класу,
 використовуючи аргументи методу як ключ для кешу. Якщо метод викликається з тими ж аргументами — повертайте вже обчислений результат із кешу.
   Якщо ні — обчислюйте та зберігайте результат у кеші."""

from functools import update_wrapper


def _cache_key(positional, kwargs):
    return (positional, tuple(sorted(kwargs.items())))


class CacheDecorator:
    """Клас-декоратор: кеш за позиційними та іменованими аргументами (без self)."""

    def __init__(self, func):
        self.func = func
        self.cache = {}
        update_wrapper(self, func)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        def bound(*args, **kwargs):
            key = (id(instance), _cache_key(args, kwargs))
            if key in self.cache:
                print("Returning cached result")
                return self.cache[key]
            print("Calculating new result")
            result = self.func(instance, *args, **kwargs)
            self.cache[key] = result
            return result

        update_wrapper(bound, self.func)
        return bound

    def __call__(self, *args, **kwargs):
        key = _cache_key(args, kwargs)
        if key in self.cache:
            print("Returning cached result")
            return self.cache[key]
        print("Calculating new result")
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        return result


@CacheDecorator
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


class MathService:
    @CacheDecorator
    def expensive_sum(self, a, b):
        return a + b


print("\n--- Task 3: CacheDecorator ---")
print(f"Fibonacci of 10: {fibonacci(10)}")
print(f"Fibonacci of 10 again: {fibonacci(10)}")

svc = MathService()
print(f"expensive_sum(2, 3): {svc.expensive_sum(2, 3)}")
print(f"expensive_sum(2, 3) again: {svc.expensive_sum(2, 3)}")
    


