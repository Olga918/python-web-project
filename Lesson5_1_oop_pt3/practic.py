#1) Створіть дескриптор PositiveValue, який:
   #Дозволяє встановлювати лише додатні числа. Використайте цей дескриптор у класі BankAccount для перевірки балансу рахунку.
   #Додайте можливість створити об’єкт BankAccount із заданим ім’ям власника та початковими коштами.
   #Якщо спробувати встановити від’ємне значення або нуль — викидається ValueError.
#Додайте ще один дескриптор Name для перевірки імені власника:
#- Ім’я має бути рядком.
#- Ім’я має містити лише літери та починатися з великої.

import json
import math
from typing import Protocol, runtime_checkable

class PositiveValue:
    """Дескриптор: дозволяє лише строго додатні числа (int або float)."""

    def __set_name__(self, owner, name):
        self._storage = f"_positive_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._storage)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("Значення має бути числом (int або float)")
        if value <= 0:
            raise ValueError("Баланс має бути додатним числом (не нуль і не від'ємне)")
        setattr(instance, self._storage, float(value) if isinstance(value, float) else value)


class Name:
    """Дескриптор: ім'я — рядок, лише літери, перша — велика."""

    def __set_name__(self, owner, name):
        self._storage = f"_name_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._storage)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("Ім'я власника має бути рядком (str)")
        if not value:
            raise ValueError("Ім'я власника не може бути порожнім")
        if not value.isalpha():
            raise ValueError("Ім'я має містити лише літери (без цифр, пробілів та інших символів)")
        if not value[0].isupper():
            raise ValueError("Ім'я має починатися з великої літери")
        setattr(instance, self._storage, value)


class BankAccount:
    owner = Name()
    balance = PositiveValue()

    def __init__(self, owner: str, initial_funds: int | float):
        self.owner = owner
        self.balance = initial_funds


#2) Створіть дескриптор LogDescriptor, який:
#   Логує кожен доступ до атрибута, включаючи читання та запис.


class LogDescriptor:
    """Логує кожне читання та запис атрибута."""

    def __set_name__(self, owner, name):
        self._storage = f"_logged_{name}"
        self._public_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(f"[LogDescriptor:{self._public_name}] read")
        return getattr(instance, self._storage)

    def __set__(self, instance, value):
        print(f"[LogDescriptor:{self._public_name}] write -> {value!r}")
        setattr(instance, self._storage, value)


class TrackedBox:
    """Приклад: атрибут під контролем LogDescriptor."""

    value = LogDescriptor()

    def __init__(self, initial):
        self.value = initial


#3) Метаклас: заборона атрибутів класу, ім'я яких починається з «приватного» підкреслення.
#   Стандартні дандери (__init__, __module__, …) дозволені — інакше клас у Python не зібрати.


class NoUnderscoreAttrsMeta(type):
    """Не дозволяє імена в просторі імен класу виду `_foo` або `__bar` (не дандер)."""

    def __new__(mcs, name, bases, namespace, **kwds):
        for key in namespace:
            if key.startswith("_") and not (key.startswith("__") and key.endswith("__")):
                raise TypeError(
                    f"Клас '{name}' не може мати атрибут '{key}', що починається з підкреслення."
                )
        return super().__new__(mcs, name, bases, namespace)


class AllowedPublic(metaclass=NoUnderscoreAttrsMeta):
    """Клас без заборонених імен у тілі — створюється нормально."""

    label = "ok"

    def __init__(self):
        self.label = "instance"


#4) Створіть метаклас, який автоматично додає в кожен клас метод hello(),
#   який виводить рядок "Hello from <ім’я класу>".


class HelloMeta(type):
    def __new__(mcs, name, bases, namespace, **kwds):
        if "hello" not in namespace:
            def hello(self):
                print(f"Hello from {type(self).__name__}")

            namespace["hello"] = hello

        return super().__new__(mcs, name, bases, namespace)


class HelloA(metaclass=HelloMeta):
    pass


class HelloB(metaclass=HelloMeta):
    value = 123


class HelloCustom(metaclass=HelloMeta):
    def hello(self):
        print(f"Hello from {self.__class__.__name__} (custom)")


#5) Метаклас: забороняє наслідування від класів, де в імені є "Forbidden".


class NoForbiddenInheritanceMeta(type):
    def __new__(mcs, name, bases, namespace, **kwds):
        forbidden = [base.__name__ for base in bases if "Forbidden" in base.__name__]
        if forbidden:
            raise TypeError(
                f"Клас '{name}' не може наслідувати {', '.join(forbidden)} "
                f"(у назві батьківського класу є 'Forbidden')."
            )
        return super().__new__(mcs, name, bases, namespace)


class AllowedBase:
    pass


class ForbiddenBase:
    pass


class ChildOk(AllowedBase, metaclass=NoForbiddenInheritanceMeta):
    pass


#6) Метаклас: усі (не службові) атрибути класу мають бути рядками.
#   Методи/дандери ігноруємо, інакше будь-який клас "зламається".


class StringAttributesOnlyMeta(type):
    def __new__(mcs, name, bases, namespace, **kwds):
        for key, value in namespace.items():
            if key == "__annotations__":
                continue
            if key.startswith("__") and key.endswith("__"):
                continue
            if callable(value) or isinstance(value, (staticmethod, classmethod, property)):
                continue
            if not isinstance(value, str):
                raise TypeError(
                    f"Клас '{name}': атрибут '{key}' має бути str, а не {type(value).__name__}."
                )
        return super().__new__(mcs, name, bases, namespace)


class AllStrings(metaclass=StringAttributesOnlyMeta):
    title = "Hello"
    status = "ok"

    def method(self):
        return self.title


#7) Протокол Shape з методом area(); фігури Circle, Rectangle, Triangle; print_area().


@runtime_checkable
class Shape(Protocol):
    def area(self) -> float:
        ...


class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius**2


class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Triangle:
    """Площа за основою та висотою: (base * height) / 2."""

    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height


def print_area(shape: Shape) -> None:
    print(shape.area())


#8) Протокол Serializable з serialize(); Person, Book → JSON; serialize_object().


@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> str:
        ...


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def serialize(self) -> str:
        return json.dumps({"name": self.name, "age": self.age}, ensure_ascii=False)


class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages

    def serialize(self) -> str:
        return json.dumps(
            {"title": self.title, "author": self.author, "pages": self.pages},
            ensure_ascii=False,
        )


def serialize_object(obj: Serializable) -> str:
    return obj.serialize()


if __name__ == "__main__":
    acc = BankAccount("Olena", 250)
    print("Owner:", acc.owner, "| balance:", acc.balance)
    acc.balance = 199.99
    print("After reassignment, balance:", acc.balance)

    try:
        BankAccount("X", 0)
    except ValueError:
        print("OK: ValueError on zero initial funds (as required).")

    try:
        acc.balance = -1
    except ValueError:
        print("OK: ValueError on negative balance (as required).")

    try:
        BankAccount("olena", 100)
    except ValueError:
        print("OK: ValueError when name does not start with uppercase.")

    try:
        BankAccount("Olena1", 100)
    except ValueError:
        print("OK: ValueError when name contains non-letters.")

    print("--- LogDescriptor demo ---")
    box = TrackedBox(10)
    _ = box.value
    box.value = 42
    print("Final value:", box.value)

    print("--- NoUnderscoreAttrsMeta ---")
    ok = AllowedPublic()
    print("AllowedPublic:", ok.label)

    _bad_namespaces = [
        ("_private field", {"__module__": __name__, "_secret": 42}),
        ("__private_name (not dunder)", {"__module__": __name__, "__internal": 1}),
        ("_method name", {"__module__": __name__, "_run": staticmethod(lambda: None)}),
    ]
    for desc, ns in _bad_namespaces:
        try:
            NoUnderscoreAttrsMeta("BadDynamic", (), ns)
        except TypeError as e:
            print("OK (" + desc + "):", type(e).__name__)

    print("--- HelloMeta ---")
    HelloA().hello()
    HelloB().hello()
    HelloCustom().hello()

    print("--- NoForbiddenInheritanceMeta ---")
    print("ChildOk created:", ChildOk.__name__)

    try:
        class BadChild(ForbiddenBase, metaclass=NoForbiddenInheritanceMeta):
            pass
    except TypeError as e:
        print("OK: TypeError on ForbiddenBase inheritance.")

    try:
        NoForbiddenInheritanceMeta(
            "BadDynamicForbidden",
            (ForbiddenBase,),
            {"__module__": __name__},
        )
    except TypeError:
        print("OK: TypeError on dynamic ForbiddenBase inheritance.")

    print("--- StringAttributesOnlyMeta ---")
    print("AllStrings.title =", AllStrings.title)

    try:
        class BadStrings(metaclass=StringAttributesOnlyMeta):
            ok = "yes"
            bad = 123
    except TypeError:
        print("OK: TypeError when attribute is not str.")

    try:
        StringAttributesOnlyMeta(
            "BadDynamicStrings",
            (),
            {"__module__": __name__, "a": "ok", "b": 1},
        )
    except TypeError:
        print("OK: TypeError on dynamic non-str attribute.")

    print("--- Shape protocol ---")
    print_area(Circle(1))
    print_area(Rectangle(2, 3))
    print_area(Triangle(4, 5))

    print("--- Serializable ---")
    print(serialize_object(Person("Olena", 25)))
    print(serialize_object(Book("Python Basics", "Ivan Petrenko", 320)))
