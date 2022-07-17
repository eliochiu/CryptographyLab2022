from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config, GlobbingFilter


# s_box生成时所用的仿射变换矩阵
shift = [[1, 0, 0, 0, 1, 1, 1, 1],
         [1, 1, 0, 0, 0, 1, 1, 1],
         [1, 1, 1, 0, 0, 0, 1, 1],
         [1, 1, 1, 1, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 0, 0],
         [0, 0, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 1, 1, 1, 1, 1]]

# 逆s_box所用的仿射矩阵
inv_shift = [[0, 0, 1, 0, 0, 1, 0, 1],
             [1, 0, 0, 1, 0, 0, 1, 0],
             [0, 1, 0, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 0, 1, 0, 0],
             [0, 1, 0, 1, 0, 0, 1, 0],
             [0, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 0, 1, 0, 1, 0, 0],
             [0, 1, 0, 0, 1, 0, 1, 0]]

# 异或向量
vector = [1, 1, 0, 0, 0, 1, 1, 0]

# 逆运算异或向量
inv_vector = [1, 0, 1, 0, 0, 0, 0, 0]


# 有限域乘
def gf_mul(a, b, poly=0x11b):
    ans = 0
    while b > 0:
        if b & 0x01 == 0x01:
            ans ^= a
            a <<= 1
        else:
            a <<= 1
        if a & 0x100 == 0x100:
            a ^= poly
            a &= 0xff
        else:
            a &= 0xff
        b >>= 1
    return ans


# 快速幂
def gf_quick_pow(a, b, poly=0x11b):
    ans = 1
    while b:
        if b & 1:
            ans = gf_mul(ans, a, poly)
        b = b >> 1
        a = gf_mul(a, a, poly)
    return ans


# 逆元
def gf_inv(a):
    return gf_quick_pow(a, 2 ** 8 - 2)


# 字节转8bit
def bytes_to_bit(n):
    res = []
    for i in range(8):
        res.append(n % 2)
        n //= 2
    return res


# 8比特转字节
def bit_to_bytes(bit_list):
    res = 0
    for i in range(8):
        res += 2 ** i * bit_list[i]
    return res


def s_box_generate():
    initial_matrix = [[16 * i + j for j in range(16)] for i in range(16)]
    for i in range(16):
        for j in range(16):
            print("0x%02x" % initial_matrix[i][j], end=' ')
        print('')
    print('')
    inv_matrix = [[0 for j in range(16)] for i in range(16)]
    res = [[0 for j in range(16)] for i in range(16)]

    for i in range(16):
        for j in range(16):
            inv_matrix[i][j] = gf_inv(initial_matrix[i][j])
            print("0x%02x" % inv_matrix[i][j], end=' ')
        print('')
    print('')
    for i in range(16):
        for j in range(16):
            list_bit = bytes_to_bit(inv_matrix[i][j])
            # print(bit_to_bytes(list_bit))
            # print(list_bit)
            tmp_list = []
            for k in range(8):
                tmp = 0
                for m in range(8):
                    if shift[k][m] == 1:
                        tmp ^= (shift[k][m] * list_bit[m]) % 2
                tmp_list.append(tmp ^ vector[k])
            res[i][j] = bit_to_bytes(tmp_list)
            print("0x%02x" % res[i][j], end=' ')
        print('')
    print('')


def inv_s_box_generate():
    initial_matrix = [[16 * i + j for j in range(16)] for i in range(16)]
    inv_matrix = [[0 for j in range(16)] for i in range(16)]
    res = [[0 for j in range(16)] for i in range(16)]
    for i in range(16):
        for j in range(16):
            list_bit = bytes_to_bit(initial_matrix[i][j])
            # print(bit_to_bytes(list_bit))
            # print(list_bit)
            tmp_list = []
            for k in range(8):
                tmp = 0
                for m in range(8):
                    if inv_shift[k][m] == 1:
                        tmp ^= (inv_shift[k][m] * list_bit[m]) % 2
                tmp_list.append(tmp ^ inv_vector[k])
            res[i][j] = bit_to_bytes(tmp_list)

    for i in range(16):
        for j in range(16):
            inv_matrix[i][j] = gf_inv(res[i][j])
            print("0x%02x" % inv_matrix[i][j], end=' ')
        print('')
    return inv_matrix


if __name__ == '__main__':
    config = Config()
    config.trace_filter = GlobbingFilter(exclude=[
        'codecs.*',
        '<*',
        'FileFinder.*',
        'ModuleLockManager.*',
        'SourceFilLoader.*'
    ])
    graphviz = GraphvizOutput()
    graphviz.output_file = 's_box.png'
    with PyCallGraph(output=graphviz, config=config):
        s_box_generate()
        inv_s_box_generate()




