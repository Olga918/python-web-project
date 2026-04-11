d = {}
print(type(d))

d = dict()
d = {"key1":"value",
     12:12,
     "d":{}}

print(d)

"""
dict:
    .values() -> повертаються значення
    .keys() -> повертаються ключі
    .items() -> повертає пари ключ:значення -> кортеж(ключ, значення)
"""

for k,v in d.items():
    print(f"{k} -> {v}")
    
for k in d.keys():
    print(k)
    
for v in d.values():
    print(v)
    
print(d[12])
d["key2"] = "hello"

print(d)

# print(d['key3']) #! KeyError: unexist key

print(len(d))

d2 = d.copy()

print(d2)

print(d2.pop("key2"))
print(d2)
print(d2.pop("key2",None))

print(d2.popitem())
print(d2)

d2.update(name="Tom", surname="Due", age=22)
# d2.update({"key1":"value1", "key2": "value2"})
print(d2)

del d2["name"]
print(d2)
# del d2["name"] #! KeyError: unexist key

print(d2.get('key3', 'NotFound'))
print(d2.get('surname', 'NotFound'))



d2.clear()
print(d2)