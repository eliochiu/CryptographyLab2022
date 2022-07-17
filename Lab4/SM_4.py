import re
import sys

'''from pycallgraph import Config, GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput'''

# s_box参数表
S_box = [0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05,
         0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
         0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62,
         0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6,
         0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8,
         0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35,
         0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87,
         0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27, 0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E,
         0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5, 0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1,
         0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55, 0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3,
         0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29, 0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F,
         0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A, 0x72, 0x6D, 0x6C, 0x5B, 0x51,
         0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8,
         0x0A, 0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8, 0xE5, 0xB4, 0xB0,
         0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84,
         0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48]

# 系统参数表
FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]

# 固定参数表
CK = [0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269, 0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
      0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249, 0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
      0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229, 0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
      0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209, 0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]


class SM4:
    def __init__(self, seed_key: int):
        # 生成轮密钥，其中K[i+4] = rk[i]
        self.round_key = self._generate_key(seed_key)

    def _generate_key(self, seed_key: int):
        # 32个轮密钥与4个初始密钥（32位）
        K = [0 for _ in range(36)]
        for i in range(4):
            K[i] = FK[i] ^ ((seed_key >> (32 * (3 - i))) & 0xffffffff)
        # 轮密钥生成
        for i in range(32):
            tmp = K[i + 1] ^ K[i + 2] ^ K[i + 3] ^ CK[i]
            tmp = self._s_box(tmp)
            tmp = self._l2(tmp)
            K[i + 4] = K[i] ^ tmp
        return K[4:]

    def _round_function(self, x_0, rk: list):
        X = [0 for _ in range(36)]
        for i in range(4):
            # 初始向量
            X[i] = (x_0 >> (32 * (3 - i))) & 0xffffffff
        # 轮函数迭代
        for i in range(32):
            tmp = X[i + 1] ^ X[i + 2] ^ X[i + 3] ^ rk[i]
            # s盒变换
            tmp = self._s_box(tmp)
            # 线性变换
            tmp = self._l1(tmp)
            X[i + 4] = X[i] ^ tmp
        # 逆序返回
        return (X[35] << 96) | (X[34] << 64) | (X[33] << 32) | X[32]

    def encryption(self, text: int):
        # 加密过程
        return self._round_function(text, self.round_key)

    def decryption(self, text: int):
        # 解密过程，逆序使用轮密钥
        return self._round_function(text, self.round_key[::-1])

    # 非线性变换s盒
    def _s_box(self, word: int):
        byte = self._word_to_bytes(word)
        res = []
        for i in range(4):
            res.append(S_box[byte[i]])
        return self._bytes_to_word(res)

    # 线性变换L
    def _l1(self, w: int):
        return w ^ self._left_rotate(w, 2) ^ self._left_rotate(w, 10) ^ self._left_rotate(w, 18) ^ self._left_rotate(w, 24)

    def _l2(self, w: int):
        return w ^ self._left_rotate(w, 13) ^ self._left_rotate(w, 23)

    # 字节转换为字（4bytes）
    @staticmethod
    def _bytes_to_word(byte: list):
        return (byte[0] << 24) | (byte[1] << 16) | (byte[2] << 8) | byte[3]

    # 字（4bytes）转换为字节
    @staticmethod
    def _word_to_bytes(n: int):
        return [(n >> 24) & 0xff, (n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff]

    # 循环左移i位
    @staticmethod
    def _left_rotate(n: int, i: int):
        return ((n << i) | (n >> (32 - i))) & 0xffffffff


# 电码本模式（electronic cipher book)
class SM4ECB:
    # 初始化密钥，加密文件路径
    def __init__(self, seed_key):
        self.seed_key = seed_key

    def encryption(self, plaintext):  # 加密
        # 生成一个sm4对象
        sm4 = SM4(self.seed_key)
        # PKCS_7填充
        plaintext = PKCS7(plaintext, 16)
        # 按16字节分组
        plaintext = re.findall(r'.{32}', plaintext)
        cipher = ''
        for i in range(len(plaintext)):
            p = int(plaintext[i], 16)
            c = hex(sm4.encryption(p))[2:].zfill(32)
            cipher += c
        return cipher

    def decryption(self, cipher):
        # 生成一个sm4对象
        sm4 = SM4(self.seed_key)
        # 按16字节分组
        cipher = re.findall(r'.{32}', cipher)
        plaintext = ''
        for i in range(len(cipher)):
            c = int(cipher[i], 16)
            p = hex(sm4.decryption(c))[2:].zfill(32)
            plaintext += p
        bytes_to_forsake = int(plaintext[-2:], 16)
        plaintext = plaintext[:-bytes_to_forsake * 2]
        return plaintext


# 密文分组链接
class SM4CBC:
    def __init__(self, seed_key, initial_vector):
        self.seed_key = seed_key
        self.initial_vector = initial_vector

    def encryption(self, plaintext):
        sm4 = SM4(self.seed_key)
        plaintext = PKCS7(plaintext, 16)
        plaintext = re.findall(r'.{32}', plaintext)
        cipher = ''
        c = 0
        for i in range(len(plaintext)):
            if i == 0:
                p = int(plaintext[i], 16) ^ self.initial_vector
                c = sm4.encryption(p)
            else:
                p = int(plaintext[i], 16) ^ c
                c = sm4.encryption(p)
            cipher += hex(c)[2:].zfill(32)
        return cipher

    def decryption(self, cipher):
        sm4 = SM4(self.seed_key)
        cipher = re.findall(r'.{32}', cipher)
        plaintext = ''
        for i in range(len(cipher)):
            c = int(cipher[i], 16)
            c_last = int(cipher[i - 1], 16)
            p = sm4.decryption(c)
            if i == 0:
                p_final = p ^ self.initial_vector
            else:
                p_final = p ^ c_last
            plaintext += hex(p_final)[2:].zfill(32)
        bytes_to_forsake = int(plaintext[-2:], 16)
        plaintext = plaintext[:-bytes_to_forsake * 2]
        return plaintext


class SM4CTR:
    def __init__(self, seed_key, initial_vector):
        self.seed_key = seed_key
        self.initial_vector = initial_vector

    def encryption(self, plaintext):
        sm4 = SM4(self.seed_key)
        plaintext = PKCS7(plaintext, 16)
        bytes_to_forsake = int(plaintext[-2:], 16)
        plaintext = re.findall(r'.{32}', plaintext)
        cipher = ''
        counter = self.initial_vector
        for i in range(len(plaintext)):
            p = int(plaintext[i], 16)
            c = p ^ sm4.encryption(counter)
            cipher += hex(c)[2:].zfill(32)
            counter += 1
        cipher = cipher[:-bytes_to_forsake * 2]
        return cipher


class SM4CFB:
    def __init__(self, seed_key, initial_vector, n):
        self.seed_key = seed_key
        self.initial_vector = initial_vector
        self.n = n

    def encryption(self, plaintext):
        # sm4对象
        sm4 = SM4(self.seed_key)
        # block_size表示一个分组内的字节数
        block_size = self.n
        # block_hex_size表示一个分组内的十六进制数的位数
        block_hex_size = 2 * block_size
        # block_bit_size表示一个分组内的二进制比特位数
        block_bit_size = 8 * block_size
        # 填充明文使其刚好能被分组n整除
        plaintext = PKCS7(plaintext, block_size)
        # 最终需要舍弃的位数
        bytes_to_forsake = int(plaintext[-2:], 16)
        # 明文分组列表
        p_list = []
        for i in range(0, len(plaintext), block_hex_size):
            p_list.append(plaintext[i: i + block_hex_size])
        # 移位寄存器
        shift = self.initial_vector
        cipher = ''
        for i in range(len(p_list)):
            o = sm4.encryption(shift)
            c = int(p_list[i], 16) ^ (o >> (128 - block_bit_size))
            cipher += hex(c)[2:].zfill(block_hex_size)
            shift = (shift << block_bit_size) | c
        cipher = cipher[:-bytes_to_forsake * 2]
        return cipher

    def decryption(self, cipher):
        sm4 = SM4(self.seed_key)
        block_size = self.n
        block_hex_size = 2 * block_size
        block_bit_size = 8 * block_size
        cipher = PKCS7(cipher, block_size)
        bytes_to_forsake = int(cipher[-2:], 16)
        c_list = []
        for i in range(0, len(cipher), block_hex_size):
            c_list.append(cipher[i: i + block_hex_size])
        shift = self.initial_vector
        plaintext = ''
        for i in range(len(c_list)):
            o = sm4.encryption(shift)
            p = int(c_list[i], 16) ^ (o >> (128 - block_bit_size))
            plaintext += hex(p)[2:].zfill(block_hex_size)
            shift = (shift << block_bit_size) | (int(c_list[i], 16))
        plaintext = plaintext[:-bytes_to_forsake * 2]
        return plaintext


class SM4OFB:
    def __init__(self, seed_key, initial_vector, n):
        self.seed_key = seed_key
        self.initial_vector = initial_vector
        self.n = n

    def encryption(self, plaintext):
        # sm4对象
        sm4 = SM4(self.seed_key)
        # block_size表示一个分组内的字节数
        block_size = self.n
        # block_hex_size表示一个分组内的十六进制数的位数
        block_hex_size = 2 * block_size
        # block_bit_size表示一个分组内的二进制比特位数
        block_bit_size = 8 * block_size
        # 填充明文使其刚好能被分组n整除
        plaintext = PKCS7(plaintext, block_size)
        # 最终需要舍弃的位数
        bytes_to_forsake = int(plaintext[-2:], 16)
        # 明文分组列表
        p_list = []
        for i in range(0, len(plaintext), block_hex_size):
            p_list.append(plaintext[i: i + block_hex_size])
        # 移位寄存器
        shift = self.initial_vector
        cipher = ''
        for i in range(len(p_list)):
            o = sm4.encryption(shift)
            selected = o >> (128 - block_bit_size)
            shift = (shift << block_bit_size) | selected
            c = int(p_list[i], 16) ^ selected
            cipher += hex(c)[2:].zfill(block_hex_size)
        cipher = cipher[:-bytes_to_forsake * 2]
        return cipher


def PKCS7(message, block_size):
    # 字节数，SM4标准使用16字节，128位的明文分组
    size = len(message) // 2
    # 待填充的字节数
    bytes_to_fill = (block_size - divmod(size, block_size)[1]) if divmod(size, block_size)[1] != 0 else block_size
    # 对字节进行填充
    for i in range(bytes_to_fill):
        message += hex(bytes_to_fill)[2:].zfill(2)
    return message


# 入口函数
def entrance1():
    # 加密的轮数
    n = int(input())
    # 输入明密文
    text = int(input().strip()[2:], 16)
    # 输入种子密钥
    seed_key = int(input().strip()[2:], 16)
    # 工作模式：加密1，解密0
    mode = int(input())
    # 调用SM_4类
    sm4 = SM4(seed_key)
    if mode == 1:
        while n:
            text = sm4.encryption(text)
            n -= 1
        print("0x%032x" % text, end='')
    elif mode == 0:
        while n:
            text = sm4.decryption(text)
            n -= 1
        print("0x%032x" % text, end='')


def entrance2():
    # 读入密钥
    seed_key = int(input()[2:], 16)
    # 加密/解密
    mode = int(input())
    # 读入明文分组
    s = sys.stdin.read().replace('\n', ' ').replace('\r', ' ').strip().split(' ')
    text = ''
    for i in range(len(s)):
        text += s[i][2:]
    # print(text)
    # 创建sm4_ecb对象
    sm4_ecb = SM4ECB(seed_key)
    res_list = []
    if mode == 1:
        res = sm4_ecb.encryption(text)
        for i in range(0, len(res), 32):
            res_list.append(res[i:i + 32])
        # print(res_list)
    else:
        res = sm4_ecb.decryption(text)
        for i in range(0, len(res), 32):
            res_list.append(res[i:i + 32])
    for res in res_list:
        for i in range(0, len(res), 2):
            print('0x' + res[i:i + 2], end=' ')
        print('')


def entrance3():
    # 读入密钥
    seed_key = int(input()[2:], 16)
    # 初始向量
    iv = int(input()[2:], 16)
    # 加密/解密
    mode = int(input())
    # 读入明文分组
    s = sys.stdin.read().replace('\n', ' ').replace('\r', ' ').strip().split(' ')
    text = ''
    for i in range(len(s)):
        text += s[i][2:]
    # 创建sm4_ecb对象
    sm4_cbc = SM4CBC(seed_key, iv)
    res_list = []
    if mode == 1:
        res = sm4_cbc.encryption(text)
    else:
        res = sm4_cbc.decryption(text)
    for i in range(0, len(res), 32):
        res_list.append(res[i:i + 32])
    for res in res_list:
        for i in range(0, len(res), 2):
            print('0x' + res[i:i + 2], end=' ')
        print('')


def entrance4():
    # 读入密钥
    seed_key = int(input()[2:], 16)
    # 初始向量
    iv = int(input()[2:], 16)
    # 加密/解密
    mode = int(input())
    # 读入明文分组
    s = sys.stdin.read().replace('\n', ' ').replace('\r', ' ').strip().split(' ')
    text = ''
    for i in range(len(s)):
        text += s[i][2:]
    # 创建sm4_ecb对象
    sm4_ctr = SM4CTR(seed_key, iv)
    res_list = []
    res = sm4_ctr.encryption(text)
    for i in range(0, len(res), 32):
        res_list.append(res[i:i + 32])
    for res in res_list:
        for i in range(0, len(res), 2):
            print('0x' + res[i:i + 2], end=' ')
        print('')


def entrance5():
    # 移位寄存器移动字节数
    n = int(input())
    # 输入密钥
    seed_key = int(input(), 16)
    # 输入初始向量
    iv = int(input(), 16)
    # 加密/解密
    mode = int(input())
    # 输入明文
    s = sys.stdin.read().replace('\n', ' ').replace('\r', ' ').strip().split(' ')

    text = ''
    for i in range(len(s)):
        text += s[i][2:]
    sm4_cfb = SM4CFB(seed_key, iv, n)
    res_list = []
    if mode == 1:
        res = sm4_cfb.encryption(text)
    else:
        res = sm4_cfb.decryption(text)
    for i in range(0, len(res), 32):
        res_list.append(res[i:i + 32])
    for res in res_list:
        for i in range(0, len(res), 2):
            print('0x' + res[i:i + 2], end=' ')
        print('')


def entrance6():
    # 移位寄存器移动字节数
    n = int(input())
    # 输入密钥
    seed_key = int(input(), 16)
    # 输入初始向量
    iv = int(input(), 16)
    # 加密/解密
    mode = int(input())
    # 输入明文
    s = sys.stdin.read().replace('\n', ' ').replace('\r', ' ').strip().split(' ')
    text = ''
    for i in range(len(s)):
        text += s[i][2:]
    sm4_ofb = SM4OFB(seed_key, iv, n)
    res_list = []
    res = sm4_ofb.encryption(text)
    for i in range(0, len(res), 32):
        res_list.append(res[i:i + 32])
    for res in res_list:
        for i in range(0, len(res), 2):
            print('0x' + res[i:i + 2], end=' ')
        print('')


if __name__ == '__main__':
    '''config = Config()
    config.trace_filter = GlobbingFilter(exclude=[
        'codecs.*',
        '<*',
        'FileFinder.*',
        'ModuleLockManager.*',
        'SourceFilLoader.*'
    ])
    graphviz = GraphvizOutput()
    graphviz.output_file = 'graph.png'
    with PyCallGraph(output=graphviz, config=config):
        '''
    entrance6()
