from math import ceil


def encryption(s, k, n):
    K = list(k)                                          # 密钥转换成列表
    l = len(s)                                           # 明文长度
    col = n                                              # 密钥长度，即矩阵的列数
    row = int(l // col)                                  # 矩阵的行数，题目保证了字符串长度整除密钥长度
    h = [['*' for j in range(col)] for i in range(row)]  # 生成一个矩阵
    c = ''                                               # 密文
    cnt = 0                                              # 将明文放置在矩阵里
    for i in range(row):
        for j in range(col):
            h[i][j] = s[cnt]
            cnt += 1
    p = sorted(range(len(K)), key=lambda i: K[i])        # 排序索引
    for j in p:                                          # 获得密文
        for i in range(row):
            c += h[i][j]
    return c


def decryption(s, k, n):
    K = [int(i) for i in list(k)]                        # 密钥转换成列表
    l = len(s)                                           # 密文长度
    col = n                                              # 密钥长度，即矩阵的列数
    row = int(l // col)                                  # 矩阵的行数
    h = [['*' for j in range(col)] for i in range(row)]  # 生成一个矩阵
    m = ''                                               # 明文
    cnt = 0
    # 将密文放置在矩阵里
    for j in range(col):
        for i in range(row):
            h[i][j] = s[cnt]
            cnt += 1
    for i in range(row):                                 # 获得密文
        for j in K:
            m += h[i][j - 1]
    return m


while True:
    n = int(input())
    k = input().replace('\n', '').replace('\r', '')
    s = input().replace('\n', '').replace('\r', '')
    mode = int(input())
    if mode == 1:
        print(encryption(s, k, n), end='\n')
    elif mode == 0:
        print(decryption(s, k, n), end='\n')

