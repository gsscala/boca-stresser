import sys

MOD = 998244353
G = 3

def power(base, exp):
    res = 1
    base %= MOD
    while exp > 0:
        if exp % 2 == 1: res = (res * base) % MOD
        base = (base * base) % MOD
        exp //= 2
    return res

def modInverse(n):
    return power(n, MOD - 2)

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j: a[i], a[j] = a[j], a[i]
        
    length = 2
    while length <= n:
        wlen = power(G, (MOD - 1) // length)
        if invert: wlen = modInverse(wlen)
        for i in range(0, n, length):
            w = 1
            for j in range(length // 2):
                u = a[i + j]
                v = (a[i + j + length // 2] * w) % MOD
                a[i + j] = (u + v) % MOD
                a[i + j + length // 2] = (u - v + MOD) % MOD
                w = (w * wlen) % MOD
        length <<= 1
        
    if invert:
        n_inv = modInverse(n)
        for i in range(n): a[i] = (a[i] * n_inv) % MOD

def multiply(a, b):
    if not a or not b: return []
    n = 1
    while n < len(a) + len(b): n <<= 1
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n): fa[i] = (fa[i] * fb[i]) % MOD
    ntt(fa, True)
    while len(fa) > 1 and fa[-1] == 0: fa.pop()
    return fa

def compose(P, Q, l, r):
    if l == r:
        return [P[l]], Q
    mid = (l + r) // 2
    p_left, q_left = compose(P, Q, l, mid)
    p_right, q_right = compose(P, Q, mid + 1, r)
    
    right_mult = multiply(q_left, p_right)
    
    p_res = p_left[:]
    if len(p_res) < len(right_mult):
        p_res.extend([0] * (len(right_mult) - len(p_res)))
    for i in range(len(right_mult)):
        p_res[i] = (p_res[i] + right_mult[i]) % MOD
        
    q_res = multiply(q_left, q_right)
    return p_res, q_res

def main():
    input_data = sys.stdin.read().split()
    if not input_data: return
    ptr = 0
    N1 = int(input_data[ptr]); ptr += 1
    P = [int(input_data[i]) for i in range(ptr, ptr + N1 + 1)]; ptr += N1 + 1
    N2 = int(input_data[ptr]); ptr += 1
    Q = [int(input_data[i]) for i in range(ptr, ptr + N2 + 1)]; ptr += N2 + 1
    
    res_p, _ = compose(P, Q, 0, N1)
    target = N1 * N2 + 1
    out = res_p + [0] * (target - len(res_p))
    print(*(out[:target]))

if __name__ == "__main__":
    main()
