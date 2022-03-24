def dec_to_hex(a):  # 将十进制数转化为十六进制序列
    return hex(a)[2:].rjust(2,'0')


def gf_plus_minus(a, b):  # GF(2**8）中的加法为模二加法，用异或实现。
    return a ^ b


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


def gf_div(a, b):  # 多项式的带余除法，返回不完全商和余数
    q = 0
    a_ini = a
    l_a, l_b = a.bit_length(), b.bit_length()
    while l_a >= l_b:
        rec = l_a - l_b
        a ^= (b << rec)
        q |= (1 << rec)
        l_a = a.bit_length()
    return q, a


def gf_ext_euclid(a, b):
    x_1, x_2 = 1, 0
    y_1, y_2 = 0, 1
    while b:
        q, r = gf_div(a, b)
        a, b = b, r
        x_1, x_2 = x_2, gf_plus_minus(x_1, gf_mul(q, x_2))
        y_1, y_2 = y_2, gf_plus_minus(y_1, gf_mul(q, y_2))
    return x_1, y_1, a


if __name__ == '__main__':
    # while True:
        s = input().split()
        a = int(s[0], 16)
        b = int(s[1], 16)
        print(dec_to_hex(gf_ext_euclid(a, b)[0]), dec_to_hex(gf_ext_euclid(a, b)[1]),dec_to_hex(gf_ext_euclid(a,b)[2]))