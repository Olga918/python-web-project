# int
# bool
# float
# str

var = 12
print(var+11)

var = "Hello"
print(var)

# + - * /, //, **, %

# Conditions

if True:
    pass
elif False:
    pass
else:
    pass

a = "True" if 5>10 else "False"
print(a)

# Cyclces
while True:
    print("While")
    break

for i in range(2):
    print("Range")

"""
Exceptions
"""

try:
    raise Exception("Unnexcepted situation")
except Exception as e:
    print(e)
finally:
    print("Finalize")

# Functions

def sample():
    print("sample function")

print(sample())

def sample_with_params(arg1:int|float, arg2:str)->tuple | None:
    print("arg1: ", arg1, "arg2: ", arg2)
    return None

# sample_with_params(arg2="Hello", arg1=12)
sample_with_params(12, arg2="Hello")