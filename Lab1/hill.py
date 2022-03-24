import copy


# 读取密钥模块
def getKeyMatrix(n):
    K = []
    for i in range(n):
        line = list(map(int, input().split()))
        K.append(line)
    return K


# 矩阵乘法模块，A为m * n矩阵，b为n * l矩阵
def matrix_dot(A, B):
    m = len(A)
    n = len(B)
    l = len(B[0])
    C = [[0 for j in range(l)] for i in range(m)]
    for i in range(m):
        for j in range(l):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                C[i][j] %= 26
    return C


# 标量乘法模块，k为标量系数
def array_dot(k, A):
    row = len(A)
    col = len(A[0])
    for i in range(row):
        for j in range(col):
            A[i][j] *= k
            A[i][j] %= 26
    return A


# 求模26的行列式模块
def det(A):
    ans = 0
    len_A = len(A)
    if len_A == 1:  # 一阶行列式
        ans = A[0][0]  # 行列式值为本身
    else:
        for i in range(len_A):  # 否则按行展开
            x = A[0][i]  # 第一行的第i列
            A_copy = copy.deepcopy(A)  # 复制一个新的A，留作计算
            del A_copy[0]  # 删掉第一行
            lu = []  # 余子式
            for j in range(1, len_A):
                del A_copy[j - 1][i]  # 删掉第j行的第i列
                lu.append(A_copy[j - 1])  # 加入到余子式当中
            ans += pow(-1, i) * x * det(lu)  # 递归，按行展开
    return ans % 26


# 求n阶方阵的伴随矩阵
def companion(A):
    len_A = len(A)
    com = [[0 for j in range(len_A)] for i in range(len_A)]
    if len_A == 1:
        return [[1]]
    else:
        for i in range(len_A):
            A_copy = copy.deepcopy(A)  # 复制一个新的A，留作计算
            del A_copy[i]
            for j in range(len_A):
                A_copy_copy = copy.deepcopy(A_copy)
                for k in range(len_A - 1):
                    del A_copy_copy[k][j]
                com[j][i] = pow(-1, i + j) * det(A_copy_copy)
    return com


# 求逆元模块
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


# 求逆矩阵模块
def inverse(A):
    D = euclid(det(A), 26)[1] % 26  # 行列式的逆元（标量值）
    return array_dot(D, companion(A))


# 加密模块
def encryption(n, K, s):
    m = [ord(i) - ord('a') for i in s]                  # 对明文进行编码
    row = int(len(m)/n)                                 # 明文矩阵行数
    col = n                                             # 明文矩阵列数
    M = [[0 for j in range(col)] for i in range(row)]   # 初始化明文矩阵
    cnt = 0                                             # 已读的明文数量
    for i in range(row):                                # 填充明文矩阵
        for j in range(col):
            M[i][j] = m[cnt]
            cnt += 1
    C = matrix_dot(M, K)                                # 计算密文矩阵
    c = ''                                              # 密文编码并读取
    for i in range(len(C)):
        for j in range(len(C[0])):
            c += chr(ord('a') + C[i][j])
    return c


# 解密模块
def decryption(n, K, s):
    c = [ord(i) - ord('a') for i in s]                  # 对密文进行编码
    row = int(len(c)/n)                                 # 明文矩阵行数
    col = n                                             # 明文矩阵列数
    C = [[0 for j in range(col)] for i in range(row)]   # 初始化明文矩阵
    cnt = 0                                             # 已读的明文数量
    for i in range(row):                                # 填充明文矩阵
        for j in range(col):
            C[i][j] = c[cnt]
            cnt += 1
    M = matrix_dot(C, inverse(K))                                # 计算密文矩阵
    m = ''                                              # 密文编码并读取
    for i in range(len(M)):
        for j in range(len(M[0])):
            m += chr(ord('a') + M[i][j])
    return m

while True:
    n = int(input())
    K = getKeyMatrix(n)
    s = input().replace('\n', '').replace('\r', '')
    mode = int(input())
    if mode == 1:
        print(encryption(n, K, s), end='\n')
    elif mode == 0:
        print(decryption(n, K, s), end='\n')

