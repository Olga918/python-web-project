l = [1,2,3,4,5]
print(l)

l2 = list("Hello")
print(l2)
print(len(l2))
print(l2[1])
print(l2[-2])

# [start:stop:step]

l3 = [i for i in range(1,100)]
print(l3)

# print(l3[0:10])
print(l3[:10])
print(l3[1:40:2])

print(l3[::-1])

for i in l2:
    print(i)
    
l2.append("Hello")
l2.append(12)
print(l2)

l2.reverse()
print(l2)

l2.extend("world")
print(l2)

print(l2.pop(4))
print(l2)

l2.insert(-1, "Last")
print(l2)

print(l2.index("Last"))
print(l2.count('l'))

newList = l2.copy()
l2.append("newItem")
print(newList)

newList.clear()
print(newList)

l2.remove(12)
print(l2)