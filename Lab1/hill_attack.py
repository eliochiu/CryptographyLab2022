import copy, random


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


def attack(n, s_m, s_c):
    m = [ord(i) - ord('a') for i in s_m]                    # 对明文进行编码
    c = [ord(i) - ord('a') for i in s_c]                    # 对密文进行编码
    row = len(m)//n
    col = n
    M_total = [[0 for j in range(col)] for i in range(row)]     # 初始化明文矩阵
    C_total = [[0 for j in range(col)] for i in range(row)]     # 初始化密文矩阵
    cnt = 0
    for i in range(row):                                    # 填充明密文矩阵
        for j in range(col):
            M_total[i][j] = m[cnt]
            C_total[i][j] = c[cnt]
            cnt += 1
    while True:
        M = []
        C = []
        rand_list = random.sample(range(row), n)             # 生成三个随机数，随机选取n行，进行已知明文攻击
        for i in range(n):
            M.append(M_total[rand_list[i]][0:])
            C.append(C_total[rand_list[i]][0:])
        flag = euclid(det(M), 26)[0]
        if flag == 1:
            break
    return matrix_dot(inverse(M),C)


def print_matrix(A, n):
    for i in range(n):
        for j in range(n):
            print(A[i][j],end=' ')
        print()


n = int(input())
m = input()
c = input()
print_matrix(attack(n,m,c),n)