import pandas as pd
from Crypto.Cipher import AES
from Crypto.Hash import keccak
from Crypto.Random import random
import numpy as np
import time


def build_trapdoor(MK, keyword):
    keyword_index = keccak.new(digest_bits=256)  # create keccak256 object
    keyword_index.update(str(keyword).encode())
    ECB_cipher = AES.new(MK.encode(), AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())


def build_codeword(ID, trapdoor):
    ID_index = keccak.new(digest_bits=256)
    ID_index.update((str(ID)+"yu7874").encode())   # "yu7874" is a custom string, i.e, "salt"
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest()).hex()  # Convert to hexadecimal and store in the index table


def build_one_index(MK, ID, keyword_list):   # keyword_list is the name of the data attribute to be searched
    secure_index = [0] * len(keyword_list)
    secure_index_temp = [0] * (len(keyword_list)-1)
    for i in range(1, len(keyword_list)):
        codeword = build_codeword(ID, build_trapdoor(MK, keyword_list[i]))
        secure_index_temp[i-1] = codeword
    random.shuffle(secure_index_temp)  # shuffle() disrupts the sequence of elements
    for j in range(1, len(keyword_list)):
        secure_index[j] = secure_index_temp[j-1]
    ID_index = keccak.new(digest_bits=256)
    ID_index.update((str(keyword_list[0])+"yu7874").encode())      # Prevent the ID from being found by the server
    # through the keccak256 hash dictionary
    secure_index[0] = ID_index.hexdigest()
    return secure_index


def build_index(raw_data_file_name, master_key, keyword_type_list):
    raw_data = pd.read_csv(raw_data_file_name)
    features = list(raw_data)
    raw_data = raw_data.values
    keyword_number = [i for i in range(0, len(features)) if features[i] in keyword_type_list]  # The column number
    # corresponding to the keyword attribute user want to query in the original file
    index_header = []
    for i in range(0, len(keyword_type_list)):
        index_header.append("index_" + str(i))

    document_index = []
    start_time = time.time()
    for row in range(raw_data.shape[0]):
        record = raw_data[row]
        record_keyword_list = [record[i] for i in keyword_number]
        record_index = build_one_index(master_key, row+1, record_keyword_list)
        document_index.append(record_index)
    random.shuffle(document_index)         # disrupt the order of each record in the index,index and plaintext are no
    # longer row to row correspondence,enhance the security
    time_cost = time.time() - start_time
    print(time_cost)
    document_index_dataframe = pd.DataFrame(np.array(document_index), columns=index_header)  # Columns indicates the
    # column name of the index file
    document_index_dataframe.to_csv(raw_data_file_name.split(".")[0] + "_index.csv")


if __name__ == "__main__":
    document_name = input("Please input the file to be encrypted:  ")
    master_key_file_name = input("Please input the file stored the master key:  ")
    master_key = open(master_key_file_name).read()
    if len(master_key) > 16:
        print("the length of master key is larger than 16 bytes, only the first 16 bytes are used")
        master_key = bytes(master_key[:16])

    keyword_list_file_name = input("Please input the file stores keyword type:  ")
    keyword_type_list = open(keyword_list_file_name).read().split(",")
    build_index(document_name, master_key, keyword_type_list)
    print("Finished")

