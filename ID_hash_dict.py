from Crypto.Hash import MD5
import time

# This program runs on the client, receives the search results sent by the server, and obtains the exact data ID
# through the dictionary corresponding to the ID and hash value. Among them, salt is added to improve the security
# of hash. MD5 in the scheme can also be replaced by sha256 with higher security.

dic = {}
dict = {}
for i in range(1, 8000):    # 4000 is the amount of data

    ID_index = MD5.new()
    ID_index.update((str(i)+"yu7874").encode())
    ID_index = ID_index.hexdigest()
    dict = {i: ID_index}
    dic.update(dict)
value = input("Please input the search results: ").split(",")
result = []
start_time = time.time()
for i in range(0, len(value)):
    va = value[i]
    x = list(filter(lambda k: dic[k] == va, dic))
    result.append(x)
print(time.time() - start_time)  # 0.005s
print(result)
