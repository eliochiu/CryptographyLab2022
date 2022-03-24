import time


def normalPow(b, n, m):
    ans = 1
    for i in range(n):
        ans = (ans * b) % m
    return ans


def quickPow(b, n, m):
    ans = 1
    b = b % m
    while n:
        if n & 1:
            ans = (ans * b) % m
        n = n >> 1
        b = (b * b) % m
    return c


if __name__ == '__main__':
    # while True:
        b, n, c = map(int, input("请输入整数b, n, c: ").split())
        print(quickPow(b, n, c))
        '''start = time.time()
        print("常规模幂算法结果:",normalPow(a, b, c))
        end = time.time()
        print("常规模幂算法时间:",end - start)

        start = time.time()
        print("快速模幂算法结果:", quickPow(a, b, c))
        end = time.time()
        print("快速模幂算法时间:",end - start)'''
