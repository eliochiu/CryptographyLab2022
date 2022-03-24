def inv(a, b):
    if b == 0:
        return 1, 0
    else:
        x1, y1 = inv(b, a % b)
        x0 = y1
        y0 = x1 - int(a // b) * y1
        return x0, y0


def remainder(m1, m2, m3, b1, b2, b3):
    M = m1 * m2 * m3
    M1 = m2 * m3
    M2 = m1 * m3
    M3 = m1 * m2
    M_1 = inv(M1, m1)[0]
    M_2 = inv(M2, m2)[0]
    M_3 = inv(M3, m3)[0]
    ans = divmod(divmod(M_1 * M1 * b1, M)[1] + divmod(M_2 * M2 * b2, M)[1] + divmod(M_3 * M3 * b3, M)[1], M)[1]
    while ans <= 0:
        ans += M
    return ans


if __name__ == '__main__':
    # while True:
        m1, m2, m3 = map(int, input().split())
        b1, b2, b3 = map(int, input().split())
        result = remainder(m1, m2, m3, b1, b2, b3)
        print(result)
