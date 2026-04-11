#1) Створіть клас Book, який має такі властивості:

#- назва книги
#- автор книги
#- кількість сторінок

#Додайте методи:

#- аксесори
#- метод, який виводить інформацію про книгу
#- метод, який повертає True, якщо кількість сторінок більше 300, інакше False.


class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.__title = title
        self.__author = author
        self.__pages = pages

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def pages(self):
        return self.__pages

    def book_info(self):
        print(f"Title: {self.title}, Author: {self.author}, Pages: {self.pages}")

    def is_long_book(self):
        return self.pages > 300


#2) Створіть клас Counter, який є лічильником:

#- count (початкове значення дорівнює 0).

#Методи:
#increment(): збільшує значення на 1,
#decrement(): зменшує значення на 1,
#reset(): скидає значення лічильника на 0,
#get_value(): повертає поточне значення лічильника.


class Counter:
    def __init__(self):
        self.__count = 0

    def increment(self):
        self.__count += 1

    def decrement(self):
        self.__count -= 1

    def reset(self):
        self.__count = 0

    def get_value(self):
        return self.__count
    

    #3) Створіть клас Calculator, який виконує прості арифметичні операції: додавання, віднімання, множення та ділення.
#Використовуйте статичні методи.

#Методи:
#add(a, b): повертає суму двох чисел,
#subtract(a, b): повертає різницю двох чисел,
#multiply(a, b): повертає добуток двох чисел,
#divide(a, b): повертає результат ділення, якщо дільник не дорівнює нулю; інакше виводить повідомлення "Ділення на нуль!".


class Calculator:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            print("Ділення на нуль!")
            return None
        return a / b
    
    #4) Створіть клас Rectangle, який має два властивості: ширина та висота.

    #Методи:
    #area(): повертає площу прямокутника,
    #perimeter(): повертає периметр прямокутника,
    #is_square(): повертає True, якщо це квадрат (ширина дорівнює висоті), інакше False.

class Rectangle:
    def __init__(self, width: float, height: float):
        self.__width = width
        self.__height = height

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height
    

    #5) Створіть клас BankAccount, який має властивості:

#- власник рахунку
#- баланс

#Методи:
#deposit(amount): збільшує баланс на amount,
#withdraw(amount): зменшує баланс на amount, якщо достатньо коштів, інакше виводить повідомлення: "Недостатньо коштів на рахунку!",
#display_balance(): виводить поточний баланс.

class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.__owner = owner
        self.__balance = balance

    @property
    def owner(self):
        return self.__owner

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount: float):
        if amount > 0:
            self.__balance += amount
        else:
            print("Сума депозиту повинна бути позитивною!")

    def withdraw(self, amount: float):
        if amount > self.__balance:
            print("Недостатньо коштів на рахунку!")
        elif amount <= 0:
            print("Сума зняття повинна бути позитивною!")
        else:
            self.__balance -= amount

    def display_balance(self):
        print(f"Баланс рахунку {self.owner}: {self.balance}")

        #6) Створіть класи Book і Library, які будуть взаємодіяти між собою.
#Клас Book:
#назва  
#автор
#кількість сторінок
#ідентифікатор книги
#Методи:
#book_info(): виводить інформацію про книгу

#Клас Library:
#список книг у бібліотеці
#Методи:
#add_book(book): додає книгу до бібліотеки
#remove_book(identifier): видаляє книгу за ідентифікатором
#find_book_by_title(title): шукає книгу за назвою та повертати її інформацію

class LibraryBook:
    def __init__(self, title: str, author: str, pages: int, identifier: str):
        self.__title = title
        self.__author = author
        self.__pages = pages
        self.__identifier = identifier

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def pages(self):
        return self.__pages

    @property
    def identifier(self):
        return self.__identifier

    def book_info(self):
        print(f"Title: {self.title}, Author: {self.author}, Pages: {self.pages}, ID: {self.identifier}")

class Library:
    def __init__(self):
        self.__books = []

    def add_book(self, book: LibraryBook):
        self.__books.append(book)

    def remove_book(self, identifier: str):
        self.__books = [book for book in self.__books if book.identifier != identifier]

    def find_book_by_title(self, title: str):
        for book in self.__books:
            if book.title == title:
                return book.book_info()
        print("Книга не знайдена!")



        #7) Створіть класи страва, замовлення та ресторан.
#Зробіть меню через яке можна робити замовлення, та оновлювати меню.
#Клас Dish:
#назва
#ціна
#категорія

#Методи:
#повертати опис страви

#Клас Order:
#список страв

#Методи:
#додати страву в замовлення
#видалити страву з замовлення
#повернути загальну суму замовлення

#Клас Restaurant:
#список доступних страв

#Методи:
#додати страву в меню
#вивести список доступних страв

class Dish:
    def __init__(self, name: str, price: float, category: str):
        self.__name = name
        self.__price = price
        self.__category = category

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def category(self):
        return self.__category

    def description(self):
        return f"{self.name} - {self.category}: ${self.price:.2f}"
    
class Order:
    def __init__(self):
        self.__dishes = []

    def add_dish(self, dish: Dish):
        self.__dishes.append(dish)

    def remove_dish(self, dish_name: str):
        self.__dishes = [dish for dish in self.__dishes if dish.name != dish_name]

    def total_price(self):
        return sum(dish.price for dish in self.__dishes)
    
class Restaurant:
    def __init__(self):
        self.__menu = []

    def add_dish_to_menu(self, dish: Dish):
        self.__menu.append(dish)

    def display_menu(self):
        print("Menu:")
        for dish in self.__menu:
            print(dish.description())



            #8) Облік студентів з файлами

#Створіть клас StudentDatabase, який зберігає студентів у файлі.
#Клас Student:
#ім'я
#вік
#оцінки

#Методи:
#повернути середню оцінку

#Клас StudentDatabase:
#додати студента у файл
#зчитати студентів з файлу
#знайти студента у файлі

class Student:
    def __init__(self, name: str, age: int, grades: list):
        self.__name = name
        self.__age = age
        self.__grades = grades

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def grades(self):
        return self.__grades

    def average_grade(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

class StudentDatabase:
    def __init__(self, filename: str):
        self.__filename = filename

    def add_student(self, student: Student):
        with open(self.__filename, 'a', encoding='utf-8') as file:
            file.write(f"{student.name},{student.age},{','.join(map(str, student.grades))}\n")

    def read_students(self):
        students = []
        try:
            with open(self.__filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    name, age, *grades = line.split(',')
                    students.append(Student(name, int(age), list(map(int, grades))))
        except FileNotFoundError:
            pass
        return students

    def find_student_by_name(self, name: str):
        students = self.read_students()
        for student in students:
            if student.name == name:
                return student
        print("Студент не знайдений!")





if __name__ == "__main__":
    print("--- Завдання 1: Book ---")
    b1 = Book("Кобзар", "Тарас Шевченко", 320)
    b1.book_info()
    print("Довга книга (>300 стор.)?", b1.is_long_book())

    b2 = Book("Казки", "Іван Франко", 120)
    b2.book_info()
    print("Довга книга (>300 стор.)?", b2.is_long_book())

    print()
    print("--- Завдання 2: Counter ---")
    c = Counter()
    print("Початкове значення:", c.get_value())
    c.increment()
    c.increment()
    print("Після increment() двічі:", c.get_value())
    c.decrement()
    print("Після decrement():", c.get_value())
    c.reset()
    print("Після reset():", c.get_value())

    print()
    print("--- Завдання 3: Calculator ---")
    print("Додавання 5 + 3 =", Calculator.add(5, 3))
    print("Віднімання 5 - 3 =", Calculator.subtract(5, 3))
    print("Множення 5 * 3 =", Calculator.multiply(5, 3))
    print("Ділення 5 / 3 =", Calculator.divide(5, 3))
    print("Ділення 5 / 0 =", Calculator.divide(5, 0))

    print()
    print("--- Завдання 4: Rectangle ---")  
    r1 = Rectangle(4, 5)
    print("Площа прямокутника 4x5:", r1.area())
    print("Периметр прямокутника 4x5:", r1.perimeter())
    print("Чи є квадратом?", r1.is_square())
    r2 = Rectangle(3, 3)
    print("Площа прямокутника 3x3:", r2.area())
    print("Периметр прямокутника 3x3:", r2.perimeter())
    print("Чи є квадратом?", r2.is_square())

    print()
    print("--- Завдання 5: BankAccount ---")
    account = BankAccount("Іван Іванов", 1000)
    account.display_balance()
    account.deposit(500)
    account.display_balance()
    account.withdraw(200)
    account.display_balance()
    account.withdraw(1500)
    account.withdraw(-100)
    account.display_balance()

    print()
    print("--- Завдання 6: Library ---")
    library = Library()
    lb1 = LibraryBook("Кобзар", "Тарас Шевченко", 320, "KB-001")
    lb2 = LibraryBook("Казки", "Іван Франко", 120, "KF-002")
    library.add_book(lb1)
    library.add_book(lb2)
    library.find_book_by_title("Кобзар")
    library.find_book_by_title("Невідома книга")
    library.remove_book(lb1.identifier)
    library.find_book_by_title("Кобзар")

    print()
    print("--- Завдання 7: Restaurant ---")
    restaurant = Restaurant()
    dish1 = Dish("Борщ", 50, "Суп")
    dish2 = Dish("Вареники", 70, "Головна страва")
    restaurant.add_dish_to_menu(dish1)
    restaurant.add_dish_to_menu(dish2)
    restaurant.display_menu()
    order = Order()
    order.add_dish(dish1)
    order.add_dish(dish2)
    print("Загальна сума замовлення:", order.total_price())
    order.remove_dish("Борщ")
    print("Загальна сума замовлення після видалення Борщу:", order.total_price())

    print()
    print("--- Завдання 8: StudentDatabase ---")
    db = StudentDatabase("students.txt")
    s1 = Student("Олександр", 20, [85, 90, 78])
    s2 = Student("Марія", 22, [92, 88, 95])
    db.add_student(s1)
    db.add_student(s2)
    students = db.read_students()
    for student in students:
        print(f"Студент: {student.name}, Вік: {student.age}, Середня оцінка: {student.average_grade():.2f}")
    found_student = db.find_student_by_name("Олександр")
    if found_student:
        print(f"Знайдений студент: {found_student.name}, Вік: {found_student.age}, Середня оцінка: {found_student.average_grade():.2f}")
            

        





