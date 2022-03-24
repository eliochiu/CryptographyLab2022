def euclid(a, b):
    (R, S, T) = (a, 1, 0)
    (R1, S1, T1) = (b, 0, 1)
    while R1 != 0:
        q = R // R1
        (tmp1, tmp2, tmp3) = (R - q * R1, S - q * S1, T - q * T1)
        (R, S, T) = (R1, S1, T1)
        (R1, S1, T1) = (tmp1, tmp2, tmp3)
    if R < 0:
        (R, S, T) = (-R, -S, -T)
    return R, S, T


def encryption(s, k, b):
    m = [ord(i) - ord('a') for i in s]  # 对明文进行编码
    if euclid(k, 26)[0] != 1:
        return 'invalid key'            # 不合法的密钥
    else:
        c = [chr((i * k + b) % 26 + ord('a')) for i in m]  # 边加密边译码
        return "".join(c)


def decryption(s, k, b):
    c = [ord(i) - ord('a') for i in s]   # 对密文进行编码
    if euclid(k, 26)[0] != 1:
        return 'invalid key'             # 不合法的密钥
    else:
        inv = euclid(k, 26)[1]           # 逆元
        m = [chr(((i - b) * inv) % 26 + ord('a')) for i in c]  # 边解密边译码
        return "".join(m)


while True:
    k, b = map(int, input().split())
    s = input().replace('\n', '').replace('\r', '')
    mode = int(input())
    if mode == 1:
        print(encryption(s, k, b), end='\n')
    elif mode == 0:
        print(decryption(s, k, b), end='\n')
