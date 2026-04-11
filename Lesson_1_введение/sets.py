s = set("Hello")
print(s)

s = {10,9,96,15,10,20,23,20}
print(s)

set1 = {1,2,3,4,5,6}
set2 = {4,5,6,7,8,9}

print(set1.union(set2))
print(set1 | set2)

print(set1.intersection(set2))
print(set1 & set2)

print(set1.difference(set2))
print(set1 - set2)

print(set2 - set1)
print(set1.symmetric_difference(set2))
print(set1 ^ set2)

print(set1.isdisjoint(set2))

set1 = {1,2,3,4}
set2 = {1,2,3,4,5,6}

print(set1.issubset(set2))
print(set2.issuperset(set1))

set1.add(10)
print(set1)

set1.remove(10)
# set1.remove(10) # KeyError: not found 10
print(set1)

set1.discard(10)
print(set1)

set1.clear()
print(set1)