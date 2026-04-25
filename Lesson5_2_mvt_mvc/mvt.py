# MVT -> Model -> View -> Template
"""
View-> render()

View.getProducts()
|
Model.getProducts -> [Product]
|
render()
|
#ProductTemplate
ProductCard
<Name>
<Price>
<Description>
|
ProductCard
Samsung s25 Ultra
$1000
New flagman by Samsung
|
"""
from abc import abstractmethod, ABC
from typing import List
from datetime import datetime

def get_current_timestamp():
    return int(datetime
               .timestamp(
                   datetime.now()
               ))


class Book:
    __id: int
    name: str
    author: str
    genre: str
    def __init__(self, name, author, genre):
        self.__id = get_current_timestamp()
        self.name = name
        self.author = author
        self.genre = genre
    @property
    def id(self):
        return self.__id
    
    
class BookModel:
    def __init__(self):
        self.books = []
    def add_book(self, book:Book):
        self.books.append(book)
    def get_books(self):
        return self.books

class BookTemplate(ABC):
    @abstractmethod
    def render(self, books:List[Book]):
        pass
    
class BooksView:
    def __init__(self, model: BookModel):
        self.model = model
    
    def render(self, template:BookTemplate):
        return template.render(self.model.get_books())
    
class BookListDetailed(BookTemplate):
    def render(self, books:List[Book]):
        if len(books) < 1:
            print("The list of books is empty")
        else:
            for i in books:
                print("-"*30)
                print(f"BookID: {i.id}")
                print(f"Name: {i.name}")
                print(f"Author: {i.author}")
                print(f"Genre: {i.genre}")
                print("-"*30, "\n")

class BookListNames(BookTemplate):
    def render(self, books:List[Book]):
        if len(books) < 1:
            print("The list of books is empty")
        else:
            print("-"*30)
            for index, item in enumerate(books, 1):
               print(f"{index}. {item.name}")
            print("-"*30, "\n")
            
def show_menu():
    print("1) Add book")
    print("2) Show detailed list of books")
    print("3) Show list of books")
    print("4) Exit")
    return int(input("Show menu item, input 1-4: "))

def create_book() -> Book:
    name = input("Enter name of book: ")
    author = input("Enter author name: ")
    genre = input("Enter genre: ")
    return Book(name, author, genre)

booksModel = BookModel()
bookView = BooksView(booksModel)

detailedList = BookListDetailed()
booksList = BookListNames()

while True:
    result = show_menu()
    
    match result:
        case 1:
            bookView.model.add_book(create_book())
        case 2: 
            bookView.render(detailedList)
        case 3: 
            bookView.render(booksList)
        case 4:
            print("Exit")
            break
        case _:
            print("Wrong menu item. Try again...")