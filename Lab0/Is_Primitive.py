# 不可约多项式集合

"""
poly = [0b110110001,
        0b101110001,
        0b110101001,
        0b101101001,
        0b100111001,
        0b101100101,
        0b110001101,
        0b101001101,
        0b100101101,
        0b100011101,
        0b111000011,
        0b101100011,
        0b110100011,
        0b110001011,
        0b100011011,
        0b110000111,
        0b100101011,
        0b111111001,
        0b111110101,
        0b111011101,
        0b110111101,
        0b111110011,
        0b101111011,
        0b111100111,
        0b111010111,
        0b101110110,
        0b111001111,
        0b110011111,
        0b101011111,
        0b100111111]
"""
# 小于四次的不可约多项式
poly = [0b10,
        0b11,
        0b111,
        0b1011,
        0b1101,
        0b11111,
        0b11001,
        0b10011]

# 记录本原多项式的个数
cnt = 0
# 存储不可约多项式
prime = []
# 存储本原多项式
primitive = []


def gf_div(a, b):  # 多项式的带余除法，返回不完全商和余数
    q = 0
    l_a, l_b = a.bit_length(), b.bit_length()
    while l_a >= l_b:
        rec = l_a - l_b
        a ^= (b << rec)
        q |= (1 << rec)
        l_a = a.bit_length()
    return q, a


def is_prime(): # 判断是否为不可约多项式
    for x in range(0x100,0x200):
        flag = 1
        for p in poly:
            if gf_div(x, p)[1] == 0:
                flag = 0
                break
        if flag:
            prime.append(x)
    return prime


def is_primitive(prime_poly): # 判断是否为本原多项式
    global cnt
    for p in prime_poly:
        flag1 = gf_div(2 ** 255 + 1, p)[1]  # 计算x^m+1除以p(x)的余数
        if flag1 == 0:  # 若余数为0，则其可能是本原本原多项式，否则一定不是本原多项式
            flag = 1    # flag = 0 ：不是本原多项式；flag = 1，为本原多项式
            for j in range(1, 255):
                flag2 = gf_div(2 ** j + 1, p)[1] # 计算x^q+1除以p(x)的余数
                if flag2 == 0:   # 若余数为0，则一定不是本原多项式
                    flag = 0
            if flag:             # 如果是1，则为本原多项式
                ans = bin(p)[2:]
                primitive.append(ans)
                cnt += 1


if __name__ == '__main__':
    is_primitive(is_prime())
    print(" ".join(primitive))
    # print(cnt)
