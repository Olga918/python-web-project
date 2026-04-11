# LEGB 
"""
- Built-in
-- Global
--- Enclosure
---- Local
"""

x = 10 # global

def sample():
    # print(x)
    x = 5 # local
    print("Local x: ", x)
    
sample()
print("Global x: ", x) # Built-in function: print

def change_global():
    global x
    x = 20
    print("Change X value:", x)
    
change_global()
print("Global x:",x)

print("-"*10, "Local variables", "-"*10)

def outer_func():
    x = 10
    print("Outer X:", x)
    
    def inner_func():
        nonlocal x
        x = 20
        print("Inner X:", x)
    
    inner_func()
    print("Outer(again) X:", x)

outer_func()

print("-"*10, "Enclosure", "-"*10)

def outer(start:int = 10):
    def inner():
        nonlocal start
        start -= 1
        print(start)
    return inner

inner = outer()

def make_storage():
    data = []
    
    push_data = lambda value: data.append(value)
    print_all_data = lambda: print(data)
    def remove_item(item):
        if item in data:
            data.remove(item)
    
    return (push_data, print_all_data, remove_item)

(push, show, delete) = make_storage()

push("Test")
show()

push(1)
push(2)
push(3)
push({"username": "admin"})

show()
delete(1)
show()