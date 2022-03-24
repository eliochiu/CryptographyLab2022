def dec_to_hex(a):  # 将十进制数转化为十六进制序列
    return hex(a)[2:].rjust(2,'0')


def gf_mul(a, b, poly = 0x11b):  # GF(2**8）中的乘法为多项式乘法
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


if __name__ == '__main__':
    # while True:
        s = input().split()
        a = int(s[0], 16)
        b = int(s[1])
        print(dec_to_hex(gf_quick_pow(a, b)))




