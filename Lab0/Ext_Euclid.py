# 计算ax+by = gcd(a,b)的一个特解x0,y0
def ext_gcd(a, b):
    R, S, T = a, 1, 0
    R1, S1, T1 = b, 0, 1
    while R1 != 0:
        q = R // R1
        tmp1, tmp2, tmp3 = R - q * R1, S - q * S1, T - q * T1
        R, S, T = R1, S1, T1
        R1, S1, T1 = tmp1, tmp2, tmp3
    if R < 0:
        R, S, T = -R, -S, -T
    return S, T, R


# 利用x0,y0计算通解
def solve(x0, y0, gcd):
    while x0 <= 0:
        if b < 0:
            x0 -= b // gcd
            y0 += a // gcd
        else:
            x0 += b // gcd
            y0 -= a // gcd
    print(x0, y0, gcd)


if __name__ == '__main__':
    # while(True):
        a, b = map(int, input().split())
        solve(ext_gcd(a, b)[0], ext_gcd(a, b)[1], ext_gcd(a, b)[2])



