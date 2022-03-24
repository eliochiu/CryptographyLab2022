# 存储每一轮要使用的轮密钥

K = ['0' for i in range(16)]

ip = (58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7)

inv_ip = (40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25)

pc_1 = (57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4)

pc_2 = (14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32)

e = (32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1)

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

p = (16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25)

round_n = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)


class DES:
    def __init__(self, initial_key: str):
        initial_key = initial_key
        self._generate_key(initial_key)

    # 密钥扩展算法
    def _generate_key(self, ini_key: str) -> None:
        global K
        key_str1 = self._permutation_choose_1(ini_key)
        C = []
        D = []
        C.append(key_str1[:28])
        D.append(key_str1[28:])
        for i in range(16):
            C.append(self.rotate_left(C[i], round_n[i]))
            D.append(self.rotate_left(D[i], round_n[i]))
            K[i] = self._permutation_choose_2(C[i + 1] + D[i + 1])

    # 轮函数
    def _round_function(self, bin_str: str, i: int) -> str:
        L, R = bin_str[:32], bin_str[32:]
        E_R = self._extend_permutation(R)
        s_in = self._o_plus(E_R, K[i])
        s_out = self._s_box_permutation(s_in)
        P_R = self._p_permutation(s_out)
        return R + self._o_plus(P_R, L)

    # 加密算法
    def encryption(self, plaintext: str) -> str:
        text_after_initial_permutation = self._initial_permutation(plaintext)
        tmp = [self._round_function(text_after_initial_permutation, 0)]
        for i in range(1, 16):
            tmp.append(self._round_function(tmp[i - 1], i))
        text_before_inv_permutation = tmp[15][32:] + tmp[15][:32]
        return self._inv_initial_permutation(text_before_inv_permutation)

    # 解密算法
    def decryption(self, ciphertext: str) -> str:
        text_after_initial_permutation = self._initial_permutation(ciphertext)
        tmp = [self._round_function(text_after_initial_permutation, 15)]
        for i in range(14, -1, -1):
            tmp.append(self._round_function(tmp[14 - i], i))
        text_before_inv_permutation = tmp[15][32:] + tmp[15][:32]
        return self._inv_initial_permutation(text_before_inv_permutation)

    # 初始置换
    def _initial_permutation(self, bin_str: str) -> str:
        return self.permutation(ip, bin_str, 64)

    # 逆初始置换
    def _inv_initial_permutation(self, bin_str: str) -> str:
        return self.permutation(inv_ip, bin_str, 64)

    # 扩展置换
    def _extend_permutation(self, bin_str: str) -> str:
        return self.permutation(e, bin_str, 48)

    # s盒置换
    def _s_box_permutation(self, bin_str: str) -> str:
        s_out_str = ''
        for i in range(8):
            input_str = bin_str[i * 6:(i + 1) * 6]
            row_str = input_str[0] + input_str[5]
            col_str = input_str[1:5]
            row_index = self.__Binary_String_to_Int(row_str)
            col_index = self.__Binary_String_to_Int(col_str)
            s_out_str += '0b{:04b}'.format(s[i][row_index][col_index])[2:]
        return s_out_str

    # p置换
    def _p_permutation(self, bin_str: str) -> str:
        return self.permutation(p, bin_str, 32)

    # 选择置换1
    def _permutation_choose_1(self, bin_str: str) -> str:
        return self.permutation(pc_1, bin_str, 56)

    # 选择置换2
    def _permutation_choose_2(self, bin_str: str) -> str:
        return self.permutation(pc_2, bin_str, 48)

    @staticmethod
    def __Binary_String_to_Int(bin_str: str) -> int:
        """
        :param bin_str: 二进制字符串
        :return: 该二进制字符串对应的整数
        """
        return int('0b' + bin_str, 2)

    @staticmethod
    def permutation(permutation_table: tuple, text: str, target_length: int) -> str:
        """
        :param permutation_table: 置换表
        :param text: 要被置换的文本
        :param target_length: 目标的置换长度
        :return: 置换后的文本字符串
        """
        permuted_str = ''
        for i in range(target_length):
            permuted_str += text[permutation_table[i] - 1]
        return permuted_str

    @staticmethod
    def rotate_left(bin_str: str, n: int) -> str:
        """
        :param bin_str: 要循环移位的字符串
        :param n: 循环移动的位数
        :return: 循环移位后的字符串
        """
        rotated_str = ''
        if n == 1:
            rotated_str = bin_str[1:] + bin_str[:1]
        if n == 2:
            rotated_str = bin_str[2:] + bin_str[:2]
        return rotated_str

    @staticmethod
    def _o_plus(bin_str_1: str, bin_str_2: str) -> str:
        """
        :param bin_str_1: 二进制字符串1
        :param bin_str_2: 二进制字符串2
        :return: 按位异或后的字符串
        """
        text_len = len(bin_str_2)
        res = ''
        for i in range(text_len):
            if bin_str_1[i] == bin_str_2[i]:
                res += '0'
            else:
                res += '1'
        return res


def __Binary_String_to_Hexadecimal(bin_str: str) -> str:
    """
    :param bin_str: 二进制字符串
    :return: 该二进制字符串对应的十六进制数
    """
    return '0x' + hex(int('0b' + bin_str, 2))[2:].rjust(16, '0')


def __Hexadecimal_to_Binary_String(hex_str: int) -> str:
    """
    :param hex_str: 十六进制数
    :return: 该十六进制数的二进制字符串（64位）
    """
    return '0b{:064b}'.format(hex_str)[2:]


# 入口函数
def entrance(target_text: int, initial_key: int, mode: int, n: int) -> str:
    initial_key = __Hexadecimal_to_Binary_String(initial_key)
    des = DES(initial_key)
    if mode == 1:
        iter_text = __Hexadecimal_to_Binary_String(target_text)
        while n != 0:
            iter_text = des.encryption(iter_text)
            n = n - 1
        return __Binary_String_to_Hexadecimal(iter_text)
    elif mode == 0:
        iter_text = __Hexadecimal_to_Binary_String(target_text)
        while n != 0:
            iter_text = des.decryption(iter_text)
            n = n - 1
        return __Binary_String_to_Hexadecimal(iter_text)


if __name__ == '__main__':
    n = int(input())
    text = int(input(), 16)
    key = int(input(), 16)
    mode = int(input())
    print(entrance(text, key, mode, n))


