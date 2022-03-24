from operator import itemgetter
import json


def create_decryption_dictionary(encrypted_filepath, dictionary_filepath):
    """
    创建一个明密文中字母频率的映射表
    保存为json文件
    """

    natural_plaintext_frequencies = [('E', 12.702),
                                     ('T', 9.056),
                                     ('A', 8.167),
                                     ('O', 7.507),
                                     ('I', 6.996),
                                     ('N', 6.749),
                                     ('S', 6.327),
                                     ('H', 6.094),
                                     ('R', 5.987),
                                     ('D', 4.253),
                                     ('L', 4.025),
                                     ('C', 2.782),
                                     ('U', 2.758),
                                     ('M', 2.406),
                                     ('W', 2.360),
                                     ('F', 2.228),
                                     ('G', 2.015),
                                     ('Y', 1.974),
                                     ('P', 1.929),
                                     ('B', 1.429),
                                     ('V', 0.978),
                                     ('K', 0.772),
                                     ('J', 0.153),
                                     ('X', 0.150),
                                     ('Q', 0.095),
                                     ('Z', 0.074)]

    encrypted_text = _readfile(encrypted_filepath)
    encrypted_text_frequencies = _count_letter_frequencies(encrypted_text)

    decryption_dict = {}
    for i in range(0, 26):
        decryption_dict[encrypted_text_frequencies[i][0]] = natural_plaintext_frequencies[i][0].lower()

    f = open(dictionary_filepath, "w")
    json.dump(decryption_dict, f)
    f.close()


def decrypt_file(encrypted_filepath, decrypted_filepath, dictionary_filepath):
    """
    用映射表对密文文件进行解密
    """

    encrypted_text = _readfile(encrypted_filepath)

    f = open(dictionary_filepath, "r")
    decryption_dict = json.load(f)
    f.close()

    decrypted_list = []

    for letter in encrypted_text:
        ascii_code = ord(letter.upper())
        if 65 <= ascii_code <= 90:
            decrypted_list.append(decryption_dict[letter])

    decrypted_text = "".join(decrypted_list)

    f = open(decrypted_filepath, "w")
    f.write(decrypted_text)
    f.close()


def _count_letter_frequencies(text):
    """
    创建一个a-z的字典来记录字母出现的次数，所有的小写字母都会变成大写字母进行处理
    所有其他字符都会被忽略
    返回按频率由高到低排序的结果
    """

    frequencies = {}
    for ascii_code in range(65, 91):
        frequencies[chr(ascii_code)] = 0

    for letter in text:
        ascii_code = ord(letter.upper())
        if 90 >= ascii_code >= 65:
            frequencies[chr(ascii_code)] += 1

    sorted_by_frequency = sorted(frequencies.items(), key=itemgetter(1), reverse=True)
    return sorted_by_frequency


def _readfile(path):
    f = open(path, "r")
    text = f.read()
    f.close()
    return text


create_decryption_dictionary("ciphertext.txt",
                             "decryption_dict.json")
decrypt_file("ciphertext.txt",
             "decrypted.txt",
             "decryption_dict.json")
print("Successful!")