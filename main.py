import random
from datetime import datetime
import os

class Encryption:
    def salt(bin_str: str) -> str:
        num_bits: int = random.randint(int(len(bin_str)/50), int(len(bin_str))) * 8
        for n in range(num_bits):
            bin_str += str(random.randint(0,1))
        salt_key: str = str(num_bits)
        return bin_str, salt_key
    
    def scramble(bin_str: str) -> str:
        scramble_hashmap = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g"
            }
        bin_scrambled_list: list = []
        bin_dict: dict = {}
        key_scramble: str = ""
        l: int = 0
        index: int = 0
        while l < len(bin_str):
            interval = random.randint(2,7)
            position = random.randint(0,int(len(bin_str)/interval))
            bin_dict[index] = bin_str[l:l+interval]
            bin_scrambled_list.insert(position, bin_str[l:l+interval])
            l += interval
            index += 1
        bin_scrambled = ''.join(bin_scrambled_list)
        i = 0
        while i < len(bin_scrambled_list):
            key_scramble += scramble_hashmap[len(str(bin_scrambled_list[i]))]
            dict_index = [key for key, value in bin_dict.items() if value == bin_scrambled_list[i]]
            key_scramble += str(dict_index[0])
            bin_dict.pop(dict_index[0])
            dict_index.clear()
            i += 1
        current_datetime = datetime.now()
        time_stamp: str = f"This encryption is paired with the key for {current_datetime}"

        return bin_scrambled, key_scramble, time_stamp

class Decryption:
    def descramble(encrypt_message: str, key: str) -> str:
        scramble_key = key.split('.')[1]
        scramble_hashmap = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7
            }
        nums_in_key: list = []
        for number in scramble_key:
            try:
                nums_in_key.append(int(number))
            except:
                nums_in_key.append('')
        decrypt_list_length: list = []
        k = len(nums_in_key) - 1
        temp_int: int = 0
        coef: int = 1
        while k > -1:
            if type(nums_in_key[k]) == int:
                temp_int += nums_in_key[k] * coef
                k -= 1
                coef *= 10
            else:
                decrypt_list_length.append(temp_int)
                temp_int = 0
                k -= 1
                coef = 1
        decrypt_list: list = [''] * (max(decrypt_list_length)+1)
        decrypt_list_length.reverse()
        i: int = 0 #scroller for encrypt_message
        j: int = 0 #scroller for scramble_key
        u: int = 0 #scroller for decrypt_list_length
        while i < len(encrypt_message):
            segment_length = scramble_hashmap[scramble_key[j]]
            segment_index = decrypt_list_length[u]
            decrypt_list[segment_index] = encrypt_message[i:i+segment_length]
            i += segment_length
            j += len(str(decrypt_list_length[u])) + 1
            u += 1
        descrambled_message: str = ''.join(decrypt_list)
        return descrambled_message
    
    def desalt(decrypt_message: str, key: str) -> str:
        salt_key: int = int(key.split(".")[0])
        desalt_message: str = decrypt_message[0:len(decrypt_message)-salt_key]
        return desalt_message

class Visualization:
    def binToAscii(bin_str: str) -> str:
        i = 0
        ascii_str = ''
        while i < len(bin_str):
            ascii_str += ''.join(chr(int(bin_str[i:i+8], 2)))
            i += 8
        return ascii_str
    
    def readFile() -> tuple:
        try:
            filename: str = input("Enter file directory: ")
        except:
            print("File directory was incorrect.")
        with open(filename, "r") as file:
            data: str = str(file.read())
        return data, filename
    
    def writeFile(encrypted_message, filename):
        file_dir: str = '/'.join(filename.split("/")[0:-1]) + "/"
        new_filename = file_dir + "encrypted" + filename.split("/")[-1]
        with open(new_filename, "w") as file:
            file.write(encrypted_message)
        return

class Main:
    #message: str = input("Enter message: ")
    message, filename = Visualization.readFile()
    
    bin_message: str = ' '.join(format(ord(x), '08b') for x in message).replace(" ", "")
    bin_salt = Encryption.salt(bin_message)
    bin_scrambled = Encryption.scramble(bin_salt[0])
    key: str = bin_salt[1] + "." + bin_scrambled[1]
    bin_descramble = Decryption.descramble(bin_scrambled[0], key)
    bin_desalt = Decryption.desalt(bin_descramble, key)

    Visualization.writeFile(Visualization.binToAscii(bin_scrambled[0]) + bin_scrambled[2], filename)

    #print(Visualization.binToAscii(bin_message))
    #print(len(bin_message))
    print(Visualization.binToAscii(bin_scrambled[0]) + bin_scrambled[2])
    #print(len(bin_scrambled[0]))
    #print(Visualization.binToAscii(bin_descramble))
    #print(Visualization.binToAscii(bin_desalt))

    if bin_message == bin_desalt:
        print("Decryption was successful")
    else:
        print("Decryption was unsuccessful")
    

if __name__ == "__main__":
    main = Main


