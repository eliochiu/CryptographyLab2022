def encryption(s, k):
    c = ''
    len_s = len(s)
    len_k = len(k)
    for i in range(len_s):
        c += chr(ord(s[i]) ^ ord(k[i % len_k]))
    return c

while True:
    k = input().replace('\n', '').replace('\r', '')
    s = input().replace('\n', '').replace('\r', '')
    mode = int(input())
    print(encryption(s, k), end='\n')
