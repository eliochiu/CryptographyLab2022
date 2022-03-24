# import time
def dec_to_hex(a):  # 将十进制数转化为十六进制序列
    return hex(a)[2:].rjust(2,'0')


def gf_mul(a, b, poly = 0x11b):  # GF(2**8）中的乘法为多项式乘法
    """
    :param a: 被乘数
    :param b: 乘数
    :return: 两数之积
    """
    ans = 0
    while b > 0:
        if b & 0x01 == 0x01:
            ans ^= a
            a <<= 1
        else:
            a <<= 1
        if a & 0x100 == 0x100:
            a ^= poly
            a &= 0xff
        else:
            a &= 0xff
        b >>= 1
    return ans


def gf_quick_pow(a, b, poly = 0x11b):
    """
    :param a: 底数
    :param b: 幂指数
    :param poly: 不可约多项式
    :return: a ^ b mod poly
    """
    ans = 1  # res: 计算结果
    while b:
        if b & 1:  # 如果 n 是奇数
            ans = gf_mul(ans, a, poly)
        b = b >> 1
        a = gf_mul(a, a, poly)
    return ans


# 对GF(2**8)的全部元素（0x00-0xff）进行穷举，来寻找使ab=1的元素b，即为a的逆元
def gf_inv1(a, poly = 0x11b):
    for i in range(1,2 ** 8):
        if gf_mul(a, i) == 1:
            return i


# 利用拉格朗日定理，若有限域的大小为N，乘法循环群的阶为N-1，则任意群的元素a，a**(N-1) = 1, 因此a的逆应为a**(N-2)
def gf_inv2(a, poly = 0x11b):
    return gf_quick_pow(a, 2 ** 8 - 2)


if __name__ == '__main__':
    # while True:
        a = int(input(), 16)
        print(dec_to_hex(gf_inv2(a)))
        '''start = time.time()
        print("穷举法结果:",dec_to_hex(gf_inv1(a)))
        end = time.time()
        print("穷举法时间:",end - start)

        start = time.time()
        print("拉格朗日定理法结果:", dec_to_hex(gf_inv2(a)))
        end = time.time()
        print("拉格朗日定理法时间:",end - start)'''

