# Immutable VS mutable
# imutable
"""
int
bool
float
str
tuple
"""
num = 4
print(type(num))

# Python створює в heap місце для значення 10, і повертає посилання, яке тепер міститься в num
num = 10 
# Ми не замінюємо число 10, воно залишається без змін, створюється новий об'єкт в heap вже зі значенням 20, і так само повертається посилання
num += 10
print(num)

st = 'HELLO'
print(st[1])
# st[1]='B'

# mutable
l1 = list("HELLO")
print(l1[1])
l1[1]='B'
print(l1)
# списки в Python не містять реальних об'єктів, це лише набір посилань на конкретні об'єкти

t = tuple([1,2,3,4,5])
print(t)
t1 = (1, )
print(t1)

print(len(t))
print(t[1])
print(t[-1])
print(t[:3])

for i in t:
    print(i)
    
print(t.index(3))
print(t.count(5))

def sample():
    num = 5
    return (1,2,3,num)

# (num,...) = sample()

# print(num)

a = 5
b = 12

(a, b) = (b, a)
print(f"{a} -> {b }")