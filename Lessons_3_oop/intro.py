print(__name__)

if __name__ == '__main__':
    # main()
    pass

from third_party import do_something

# do_something()

"""
1 variant: if we have a base classes
class <ClassName>(base_class1, base_class2):
    pass

2 variant: if we don`t have a base classees
class <ClassName>:
    pass
"""

# object -> Class -> your_instance

# Example: 

class Student:
    # constructor
    def __init__(self, name:str, surname:str, university:str, group_name:str):
        # private field: self.__<field_name>
        # self.name = name # public name
        self.__name = name # private
        self.surname = surname
        self.university = university
        self.group_name = group_name
    
    def set_name(self, value):
        self.__name = value
        
    def get_name(self):
        return self.__name
    
    def __str__(self):
        return f"""
    -----------------------------
    Name: {self.__name}
    Surname: {self.surname}
    University: {self.university}
    Group: {self.group_name}
    -----------------------------
    """
    
print('-'*10,'Create class object','-'*10)

s = Student('Ivan', 'Petrov', 'OTUS', 'KN-212')

print(s._Student__name)


# print(s.name)
print(s.get_name())
# s.name = 'Volodymyr'
# print(s.name)
# print(s)

print(s.__dict__)

s.age = 21
print(s.age)
print(s.__dict__)

s1 = Student("n1", "s1", 'u1', 'g1')
print(s1)
print("s1 dict: ", s1.__dict__)

# Slots
print('-'*10,'Slots','-'*10)

class Point:
    __slots__ = ("__x","__y")
    
    def __init__(self, x:float, y:float):
        self.__x = x
        self.__y = y
    
    @classmethod
    def point_method(cls, data:str):
        x, y = data.split('-')
        return cls(float(x), float(y))
      
    @staticmethod
    def get_instance(x:float = 0, y:float = 0):
        return Point(x,y)
    
    @property
    def X(self):
        print("Getter X")
        return self.__x
    
    @X.setter
    def X(self, value):
        if value < 0:
            raise ValueError("X can't be less than zero.")
        self.__x = value
    
    def __str__(self):
        return f"[{self.__x}, {self.__y}]"
    
    def set_y(self, value):
        if value < 0:
            raise ValueError("Y can't be less than zero.")
        self.__y = value
    
    Y = property(
        lambda self: self.__y,
        set_y,
        None,
        "This property can change or get Y coord for Point"
    )
    
p = Point(1.5, 3.5)

print(p)
# p.z = 5.5 #! Error: ми не можемо задавати нові властивості, тому що словник був замінений на слоти, які не дозволяють додавати нові атрибути.
# p.__dict__ #! Помилка: словника атрибутів більше немає, заміщений слотами.
print(p.__slots__)
# print(p.z)


print('-'*10,'Properties','-'*10)
print("X:",p.X)
print("Y:",p.Y)
p.Y = 10.5
print(p)

# p.Y = -1 #! Error

p = Point.get_instance()

print(p)

p = Point.point_method("10.5-19.6")
print(p)