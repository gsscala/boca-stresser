import sys
from bisect import bisect_left

MOD = 998244353

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

class SegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [1] * (4 * n + 1)

    def update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val % MOD
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(2 * node, start, mid, idx, val)
        else:
            self.update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = (self.tree[2 * node] * self.tree[2 * node + 1]) % MOD

    def query(self, node, start, end, l, r):
        if r < start or end < l or l > r:
            return 1
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        p1 = self.query(2 * node, start, mid, l, r)
        p2 = self.query(2 * node + 1, mid + 1, end, l, r)
        return (p1 * p2) % MOD

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    K = int(input_data[1])
    T = [0] * (N + 1)
    occ = [[] for _ in range(N + 1)]
    last = [0] * (N + 1)
    
    for i in range(1, N + 1):
        t = int(input_data[i+1])
        T[i] = t
        occ[t].append(i)
        last[t] = i
        
    st = SegTree(N)
    C = [0] * (N + 1)
    pool_end = 0
    ans = 0
    
    for j in range(1, N + 1):
        max_pool = max(0, j - K - 1)
        while pool_end < max_pool:
            pool_end += 1
            t_type = T[pool_end]
            C[t_type] += 1
            st.update(1, 1, N, last[t_type], C[t_type] + 1)
            
        if j == last[T[j]]:
            search_val = max(1, j - K)
            idx = bisect_left(occ[T[j]], search_val)
            pos = occ[T[j]][idx]
            limit = pos + K + 1
            
            waysA = 0
            if C[T[j]] > 0:
                prodA = st.query(1, 1, N, 1, j - 1)
                waysA = (C[T[j]] * prodA) % MOD
                
            query_limit = min(N, limit - 1)
            prodB_full = st.query(1, 1, N, 1, query_limit)
            waysB = (prodB_full * modInverse(C[T[j]] + 1)) % MOD
            
            ans = (ans + waysA + waysB) % MOD
            
    print(ans)

if __name__ == "__main__":
    main()
