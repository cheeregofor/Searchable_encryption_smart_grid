from Crypto.Cipher import AES
from Crypto.Hash import keccak
import time

def build_trapdoor(MK, keyword):
    keyword_index = keccak.new(digest_bits=256)
    keyword_index.update(keyword.encode())
    ECB_cipher = AES.new(MK.encode(), AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())

if __name__ == "__main__":

    keyword = input("Please input the keyword you want to search:  ")

    master_key_file_name = input("Please input the file stored the master key:  ")
    master_key = open(master_key_file_name).read()
    if len(master_key) > 16:
        print("the length of master key is larger than 16 bytes, only the first 16 bytes are used")
        master_key = bytes(master_key[:16])


    trapdoor_file = open(keyword + "_trapdoor", "wb+")
    start_time = time.time()
    trapdoor_of_keyword = build_trapdoor(master_key, keyword)
    print(time.time() - start_time)
    trapdoor_file.write(trapdoor_of_keyword)
    trapdoor_file.close()
