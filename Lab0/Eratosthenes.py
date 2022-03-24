flag = 2000000 * [0]
prime = 100000 * [0]


def eratosthenes_test(n):            # 输出2到n的全部素数
    cnt = 0                          # 当前已判断出的素数的数量
    for i in range(2, n + 1):
        j = 0
        if flag[i] == 0:             # 如果当前i为素数
            prime[cnt] = i           # 将i加入到prime中
            cnt += 1                 # 素数数量加一
        while (j < cnt) and (i * prime[j] <= n):
            flag[i * prime[j]] += 1  # 筛掉列表prime中现有素数的倍数
            if i % prime[j] == 0:
                break
            j += 1

# 第一次筛掉4，加入2
# 第二次筛掉6和9，加入3
# 第三次筛掉8和12，不加入
# 第四次筛掉10、15，加入5


if __name__ == '__main__':
    # while True:
        n = int(input())
        eratosthenes_test(n)
        print(" ".join(str(i) for i in prime if i != 0))
