import pandas as pd
from Crypto.Cipher import AES
import time
from bitarray import bitarray
import binascii


def build_codeword(ID, trapdoor):
    rs = binascii.unhexlify(ID)
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(rs).hex()


def BKDRHash(X):
    seed = 31  # 131
    hash = 0
    i = 0
    while i < 5 and X[i]:
        hash = hash * seed + ord(X[i])
        i = i + 1
    return (hash & 0x7FFFFFFF) % 907    # 907 can be replaced by other prime numbers


def creat_bloom(codeword_list):
    bloom_array = 907*bitarray("0")
    for i in range(len(codeword_list)):
        num1 = BKDRHash(codeword_list[i])
        bloom_array[num1] = True
    return bloom_array


def build_bloom(index_file_name):
    document_index = []

    data_index = pd.read_csv(index_file_name)
    data_index = data_index.values
    clo = data_index.shape[1]
    start_time = time.time()
    for row in range(data_index.shape[0]):
        record = data_index[row]
        data_list = [record[i] for i in range(2, clo)]  # start from 2, as 0 is order number, 1 is ID hash
        gh = creat_bloom(data_list)  # 2
        document_index.append(gh)
    time_cost = time.time() - start_time
    print(time_cost)
    return document_index        # For a index file, server only needs to calculate the bloom index once, which can be
    # stored in memory and used for many times, and is not calculated in the search time


def bloom_search(trapdoor, index):
    li = build_bloom(index)
    search_result = []
    data_index2 = pd.read_csv(index)
    data_index2 = data_index2.values
    start_time = time.time()
    for row in range(len(li)):
        record = li[row]
        record2 = data_index2[row]
        ID_code = build_codeword(record2[1], trapdoor)
        num1 = BKDRHash(ID_code)
        if record[num1] and ID_code in data_index2[row]:
                search_result.append(record2[1])
    print(time.time() - start_time)
    print(search_result)


if __name__ == "__main__":
    trapdoor = input("Please input the trapdoor file:  ")
    trapdoor = open(trapdoor, "rb").read().strip()
    index = input("Please input the index file:  ")
    bloom_search(trapdoor, index)
