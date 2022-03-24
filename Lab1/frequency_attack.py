def attack(s):
    alphabet = []                         # 字母频数表
    for i in range(26):                   # 统计字母频数
        letter = chr(i + ord('a'))
        alphabet.append(s.count(letter))  # 生成字母频数表，其中alphabet[0]代表a出现的频数
    # 倒序排列，找出出现频率最高的密文字母
    p = sorted(range(len(alphabet)), key=lambda i: alphabet[i], reverse=True)
    top = []
    for i in range(len(p)):
        top.append(chr(p[i] + ord('a')))
    # 这里取频率最高的三个密文字母
    c = [top[0], top[1]]
    # 英文文本里出现频率最高的三个明文字母
    m = ['e', 't']
    # 创建判断矩阵
    judge_matrix = [[0 for j in range(2)] for i in range(2)]
    for i in range(2):
        for j in range(2):
            judge_matrix[i][j] = (ord(c[i]) - ord(m[j])) % 26

    if judge_matrix[0][0] == judge_matrix[1][1]:
        return judge_matrix[0][0]
    elif judge_matrix[0][1] == judge_matrix[1][0]:
        return judge_matrix[0][1]


s = list(input().replace('\n', '').replace('\r', ''))
print(attack(s), end='')