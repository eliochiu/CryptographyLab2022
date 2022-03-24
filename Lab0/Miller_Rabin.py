import random


def is_prime(n, trials=100):
    # n为要进行素性检测的数，trials为测试的次数
    assert n >= 2
    # 当n为2时，n是素数
    if n == 2:
        return True
    # 当n为大于2的偶数时，n为合数
    if n & 1 == 0:
        return False
    # 把n-1写成(2^s)*d的形式
    s = 0
    d = n - 1
    while True:
        q, r = divmod(d, 2)
        if r == 1:
            break
        s += 1
        d = q
    assert (2 ** s * d == n - 1)

    # 测试以a为底时，n是否为合数
    def is_witness(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True
    # 以上条件都不满足时，n一定是合数

    # 尝试trials次
    for i in range(trials):
        a = random.randrange(2, n)
        if is_witness(a):
            return False
    return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # while True:
        n = int(input())
        if is_prime(n):
            print("YES")
        else:
            print("NO")
