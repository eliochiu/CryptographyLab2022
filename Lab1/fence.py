from math import ceil


def encryption(s, n):
    l = len(s)                                           # 明文串的长度
    m = ceil(l / n)                                      # 向上取整的列数，生成一个n行，m列的栅栏
    fence = [['*' for i in range(m)] for j in range(n)]  # 生成一个n行m列的栅栏
    c = []                                               # 按照列的顺序将明文放置在栅栏里
    cnt = 0                                              # cnt记录已经放置的字符数
    for j in range(m):                                   # 先将明文字母按列填充
        for i in range(n):                               # 一列放满再换下一列
            if cnt < l:                                  # 还未放完全部字符
                fence[i][j] = s[cnt]
                cnt += 1
    for i in range(n):                                   # 按照先行后列的方法获得密文
        for j in range(m):
            if fence[i][j] != '*':                       # 有效字符就输出
                c.append(fence[i][j])
    return ''.join(c)


def pre_processing(s, n):
    len_s = len(s)                                       # 密文长度
    m = ceil(len_s / n)                                  # n为列数，得到一个n行m列的栅栏
    target_length = n * m                                # 栅栏的总格数
    tripped = []                                         # 补位字符串列表
    while len_s < target_length:                         # 循环
        s += '*'                                         # 在密文串后面补 *
        tripped.append(s[-m:])                           #
        s = s[:-m]
        len_s += 1
    tripped.reverse()
    tripped_str = ''.join(tripped)
    result = s + tripped_str
    return result


def decryption(s, n):
    s = pre_processing(s, n)                            # 对密文进行补位处理
    l = len(s)                                          # 密文串的长度
    m = ceil(l / n)                                     # 向上取整的列数，生成一个n行，m列的栅栏
    h = [['*' for i in range(m)] for j in range(n)]
    ms = []                                             # 按照先行后列的方法将密文放置在栅栏里
    k = 0
    for i in range(n):
        for j in range(m):
            if k < l:
                h[i][j] = s[k]
                k += 1
    # 按照先列后行的方法获得明文
    for i in range(m):
        for j in range(n):
            if h[j][i] != '*':
                ms.append(h[j][i])
    return ''.join(ms)


while True:
    n = int(input())
    s = input().replace('\n', '').replace('\r', '')
    mode = int(input())
    if mode == 1:
        print(encryption(s, n), end='\n')
    elif mode == 0:
        print(decryption(s, n), end='\n')
