def encryption(s, k):
    c = []
    m = [ord(i) - ord('a') for i in s]  # 对明文进行编码
    K = [ord(i) - ord('a') for i in k]  # 对密钥进行编码
    l_m = len(m)                        # 明文长度
    l_k = len(K)                        # 密钥长度
    for i in range(l_m):
        tmp = (m[i] + K[i % l_k]) % 26
        c.append(chr(tmp + ord('a')))
    return "".join(c)


def decryption(s, k):
    m = []
    c = [ord(i) - ord('a') for i in s]  # 对密文进行编码
    K = [ord(i) - ord('a') for i in k]  # 对密钥进行编码
    l_c = len(c)                        # 密文长度
    l_k = len(K)                        # 密钥长度
    for i in range(l_c):
        tmp = (c[i] - K[i % l_k]) % 26
        m.append(chr(tmp + ord('a')))
    return "".join(m)


while True:
    k = input().replace('\n', '').replace('\r', '')
    s = input().replace('\n', '').replace('\r', '')
    mode = int(input(''))
    if mode == 1:
        print(encryption(s, k), end='\n')
    elif mode == 0:
        print(decryption(s, k), end='\n')


