# class A(<tuple_of_base_classes>)


#    A
#  /    \
#B      C
# \     /
#    D


class A:
    def __init__(self):
        print("Constructor A")
    def method(self):
        print("class A")

class B(A):
    def __init__(self):
        print("Constructor B")
    def method(self):
        print("class B")
        
class C(A):
    def __init__(self):
        print("Constructor C")
    def method(self):
        print("class C")
        
class D(C, B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        C.__init__(self)
    # def __init__(self):
    #     print("Constructor D")
    def method(self):
        print("class D")
        
D().method()

# D().method2()

# MRO - Method Resolution Order

print(D.mro())

from datetime import datetime


class UploadFileMixin:
    def save(self):
        print(f"Save {self.__class__.__name__} {self.__dict__.get("username", None)} to file")

class LoggerMixin:
    def log(self, message):
        print(f"[LOG]|{self.__class__.__name__}|{datetime.now()}|{message}")

class User(LoggerMixin, UploadFileMixin):
    def __init__(self, username):
        self.username = username
    
    def login(self):
        self.log(f"User: [{self.username}] trying to login")
        self.save()
        
User("Mark").login()

# BaseUser -> (Creds, FullName) BaseUser(PermisionsMixin) -> list[Permisions], isSuperUser:bool