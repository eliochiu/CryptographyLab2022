def gcd(a, b):
    # 只考虑正数的最大公因子计算
    a, b = abs(a), abs(b)
    if a < b:
        a, b = b, a
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


if __name__ == '__main__':
    # while(True):
        a, b = map(int, input().split())
        print("gcd({a}, {b}) = {g}".format(a = a, b = b, g = gcd(a,b)))




