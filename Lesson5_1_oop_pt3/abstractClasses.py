from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak():
        pass

class Tiger(Animal):
    def speak():
        print("RrrfrrrrRRR!")
        
Tiger()

from typing import Protocol, List, runtime_checkable

@runtime_checkable
class Printable(Protocol):
    def print_console(self):
        pass
    
    def print_file(self):
        pass
    
class B(Printable):
    field1:str = "Hello"
    field2:float = 3.15
    
    def print_console(self):
        print("field1:", self.field1)
        print("field2:", self.field2)
    
    def print_file(self):
        with open('B.txt', 'w+') as file:
            file.write(f"field1: {self.field1}")
            file.write(f"field2: {self.field2}")
            
def check_protocol(collection: List[Printable]):
    for item in collection:
        if isinstance(item, Printable):
            item.print_console()
            item.print_file()

class A:
    pass

objects = [A(), B(), A()]
check_protocol(objects)