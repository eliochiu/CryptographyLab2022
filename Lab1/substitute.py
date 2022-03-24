def encryption(ini_table, sub_table, m):
    c = []
    for i in m:
        pos = ini_table.index(i)      # 找到明文字母i在原始表中的位置
        c.append(sub_table[pos])      # 替换成密文字母
    return "".join(c)


while True:
    ini_table = input().replace('\n', '').replace('\r', '')              # 原字母表
    sub_table = input().replace('\n', '').replace('\r', '')              # 代替表
    s = input().replace('\n', '').replace('\r', '')                      # 明文/密文
    mode = int(input())                                                  # 加密模式
    if mode == 1:
        print(encryption(ini_table, sub_table, s), end='\n')
    elif mode == 0:
        print(encryption(sub_table, ini_table,s),end='\n')