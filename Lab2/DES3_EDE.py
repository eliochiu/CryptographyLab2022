# 存储每一轮要使用的轮密钥
K = ['0' for i in range(16)]


def __Binary_String_to_Int(bin_str):
    """
    :param bin_str: 二进制字符串
    :return: 该二进制字符串对应的整数
    """
    return int('0b' + bin_str, 2)


def __Hexadecimal_to_Binary_String(hex_str):
    """
    :param hex_str: 十六进制数
    :return: 该十六进制数的二进制字符串（64位）
    """
    return '0b{:064b}'.format(hex_str)[2:]


def __Binary_String_to_Hexadecimal(bin_str):
    """
    :param bin_str: 二进制字符串
    :return: 该二进制字符串对应的十六进制数
    """
    return '0x' + hex(int('0b' + bin_str, 2))[2:].rjust(16, '0')


# 置换选择1
def P_1(bin_str):
    """
    :param bin_str: 初始密钥（56bit）
    :return: 选择置换1后的结果（56bit）
    """
    pc_1 = (57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4)
    permuted_str = ''
    for i in range(56):
        permuted_str += bin_str[pc_1[i] - 1]
    return permuted_str


# 置换选择2
def P_2(bin_str):
    """
    :param bin_str: 循环左移后的密钥（56bit）
    :return: 选择置换2后的结果（48bit）
    """
    pc_2 = (14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32)
    permuted_str = ''
    for i in range(48):
        permuted_str += bin_str[pc_2[i] - 1]
    return permuted_str


# 循环左移n位
def Rotate_Left(bin_str, n):
    """
    :param bin_str: 经过选择置换1后的结果，拆分为两部分（28bit）
    :param n: 循环左移的位数（1或2，由轮数决定）
    :return:
    """
    rotated_str = ''
    if n == 1:
        rotated_str = bin_str[1:] + bin_str[:1]
    if n == 2:
        rotated_str = bin_str[2:] + bin_str[:2]
    return rotated_str


# 密钥扩展算法
def Generate_Key(key_str):
    """
    :param key_str: 初始输入密钥key_str（64bit）
    :return: 16轮的全部密钥列表K
    """
    global K
    round_n = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)
    key_str1 = P_1(key_str)
    C = []
    D = []
    C.append(key_str1[:28])
    D.append(key_str1[28:])
    for i in range(16):
        C.append(Rotate_Left(C[i], round_n[i]))
        D.append(Rotate_Left(D[i], round_n[i]))
        K[i] = P_2(C[i + 1] + D[i + 1])


# 初始置换
def IP(bin_str):
    """
    初始置换IP
    :param bin_str: 输入的二进制明文字符串（64bit）
    :return: 置换后的二进制字符串permuted_str（64bit）
    """
    ip = (58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7)

    permuted_str = ''
    for i in range(64):
        permuted_str += bin_str[ip[i] - 1]
    return permuted_str


# 初始逆置换
def Inv_IP(bin_str):
    """
    :param bin_str: 输入加密后的密文二进制字符串（64bit）
    :return: 逆置换后的二进制字符串permuted_str（64bit）
    """
    inv_ip = (40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25)

    permuted_str = ''
    for i in range(64):
        permuted_str += bin_str[inv_ip[i] - 1]
    return permuted_str


# 扩展置换E
def E(bin_str):
    """
    :param bin_str: 输入初始置换后的明文字符串的右半侧（32bit）
    :return: 扩展置换后的二进制字符串（48bit）
    """
    e = (32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1)
    extend_permuted_str = ''
    for i in range(48):
        extend_permuted_str += bin_str[e[i] - 1]
    return extend_permuted_str


# s盒代替
def S_Box(bin_str):
    """
    :param bin_str: 输入扩展置换与密钥异或后的字符串（48bit）
    :return: s盒选择压缩变换（32bit）
    """
    s = [
        # S1
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        # S2
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        # S3
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        # S4
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        # S5
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        # S6
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        # S7
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        # S8
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

    s_out_str = ''
    for i in range(8):
        input_str = bin_str[i * 6:(i + 1) * 6]
        row_str = input_str[0] + input_str[5]
        col_str = input_str[1:5]
        row_index = __Binary_String_to_Int(row_str)
        col_index = __Binary_String_to_Int(col_str)
        s_out_str += '0b{:04b}'.format(s[i][row_index][col_index])[2:]
    return s_out_str


# 选择置换P
def P(bin_str):
    """
    :param bin_str: 输入s盒选择压缩变换后的字符串（32bit）
    :return: F函数的最终运算结果（32bit）
    """
    p = (16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25)

    permuted_str = ''
    for i in range(32):
        permuted_str += bin_str[p[i] - 1]
    return permuted_str


# 轮函数
def F(input_str, i):
    """
    :param input_str: 轮函数输入字符（64bit）
    :param i: 第i轮（i=0～15）
    :return: 第i轮的加密结果（64bit）
    """
    L, R = input_str[:32], input_str[32:]
    E_R = E(R)
    s_in = __Binary_String_to_Int(E_R) ^ __Binary_String_to_Int(K[i])
    s_out = S_Box('0b{:048b}'.format(s_in)[2:])
    P_R = P(s_out)
    return R + '0b{:032b}'.format(__Binary_String_to_Int(P_R) ^ __Binary_String_to_Int(L))[2:]


# 加解密算法
def DES_Encryption(plaintext, initial_key):
    """
    :param plaintext: 明文（64位）
    :param initial_key: 初始密钥（64位）
    :return: 密文（64位）
    """

    text_after_initial_permutation = IP(plaintext)
    Generate_Key(initial_key)
    tmp = []
    tmp.append(F(text_after_initial_permutation, 0))
    for i in range(1, 16):
        tmp.append(F(tmp[i - 1], i))
    text_before_inv_permutation = tmp[15][32:] + tmp[15][:32]
    return Inv_IP(text_before_inv_permutation)


def DES_Decryption(ciphertext, initial_key):
    """
    :param ciphertext: 密文（64位）
    :param initital_key: 初始密钥（64位）
    :return: 明文（64位）
    """
    text_after_initial_permutation = IP(ciphertext)
    Generate_Key(initial_key)
    tmp = []
    tmp.append(F(text_after_initial_permutation, 15))
    for i in range(14, -1, -1):
        tmp.append(F(tmp[14 - i], i))
    text_before_inv_permutation = tmp[15][32:] + tmp[15][:32]
    return Inv_IP(text_before_inv_permutation)


def EDE_Encryption(plaintext, k_1, k_2):
    plaintext = __Hexadecimal_to_Binary_String(plaintext)
    res1 = DES_Encryption(plaintext, k_1)
    res2 = DES_Decryption(res1, k_2)
    res3 = DES_Encryption(res2, k_1)
    return __Binary_String_to_Hexadecimal(res3)


def EDE_Decryption(ciphertext, k_1, k_2):
    ciphertext = __Hexadecimal_to_Binary_String(ciphertext)
    res1 = DES_Decryption(ciphertext, k_1)
    res2 = DES_Encryption(res1, k_2)
    res3 = DES_Decryption(res2, k_1)
    return __Binary_String_to_Hexadecimal(res3)


def EDE_DES():
    text = int(input(), 16)
    key_1 = int(input(), 16)
    key_2 = int(input(), 16)
    k_1 = __Hexadecimal_to_Binary_String(key_1)
    k_2 = __Hexadecimal_to_Binary_String(key_2)
    mode = int(input())
    if mode == 1:
        print(EDE_Encryption(text, k_1, k_2))
    elif mode == 0:
        print(EDE_Decryption(text, k_1, k_2))


EDE_DES()
