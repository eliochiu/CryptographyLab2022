def dec_to_hex(a):  # 将十进制数转化为十六进制序列
    return hex(a)[2:].rjust(2, '0')


def gf_plus_minus(a, b):  # GF(2**8）中的加法为模二加法，用异或实现。
    """
    :param a: 被加数/被减数
    :param b: 加数/减数
    :return: 两数之和/差
    """
    return a ^ b


def gf_mul(a, b, poly=0x11b):  # GF(2**8）中的乘法为多项式乘法
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


def gf_div(a, b):  # 多项式的带余除法，返回不完全商和余数
    """
    :param a: 被除数
    :param b: 除数
    :return: 不完全商和余数
    """
    q = 0
    l_a, l_b = a.bit_length(), b.bit_length()
    while l_a >= l_b:
        rec = l_a - l_b
        a ^= (b << rec)
        q |= (1 << rec)
        l_a = a.bit_length()
    return q, a


def gf_cal(op, a, b):
    if op == '+' or op == '-':
        print(dec_to_hex(gf_plus_minus(a, b)))
    elif op == '*':
        print(dec_to_hex(gf_mul(a, b)))
    else:
        print(dec_to_hex(gf_div(a, b)[0]), dec_to_hex(gf_div(a, b)[1]))


if __name__ == '__main__':
    # while True:
        s = input().split()
        a = int(s[0], 16)
        b = int(s[2], 16)
        op = s[1]
        gf_cal(op, a, b)
