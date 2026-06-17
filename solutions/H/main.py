import sys

class BIT:
    def __init__(self, n):
        self.size = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        while i <= self.size:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def query_range(self, l, r):
        if l > r:
            return 0
        return self.query(r) - self.query(l - 1)

def sum_block(B, L_pos, R_pos, K, offset_val, P, bit):
    length = R_pos - L_pos + 1
    base_sum = length * B * K
    idx_L = (L_pos + offset_val) % K
    idx_R = (R_pos + offset_val) % K
    
    if idx_L <= idx_R:
        p_sum = bit.query_range(idx_L + 1, idx_R + 1)
    else:
        p_sum = bit.query_range(idx_L + 1, K) + bit.query_range(1, idx_R + 1)
    
    return base_sum + p_sum

def query_range(l, r, K, offset_val, P, bit):
    B_L, pos_L = divmod(l, K)
    B_R, pos_R = divmod(r, K)
    
    if B_L == B_R:
        return sum_block(B_L, pos_L, pos_R, K, offset_val, P, bit)
    
    ans = sum_block(B_L, pos_L, K - 1, K, offset_val, P, bit)
    ans += sum_block(B_R, 0, pos_R, K, offset_val, P, bit)
    
    if B_R - B_L > 1:
        num = B_R - B_L - 1
        A = B_L + 1
        B = B_R - 1
        p_full = K * (K - 1) // 2
        ans += num * p_full
        
        A_plus_B = A + B
        sum_arithmetic = (A_plus_B * num) // 2
        base_full = K * K * sum_arithmetic
        ans += base_full
        
    return ans

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    Q = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
    P = list(range(K))
    bit = BIT(K)
    for i in range(K):
        bit.update(i + 1, i)
        
    offset_val = 0
    results = []
    
    for _ in range(Q):
        tipo = int(input_data[ptr]); ptr += 1
        if tipo == 1:
            p = int(input_data[ptr]); ptr += 1
            offset_val = (offset_val + p) % K
        elif tipo == 2:
            s = int(input_data[ptr]); ptr += 1
            t = int(input_data[ptr]); ptr += 1
            idx_s = (s + offset_val) % K
            idx_t = (t + offset_val) % K
            val_s = P[idx_s]
            val_t = P[idx_t]
            P[idx_s] = val_t
            P[idx_t] = val_s
            bit.update(idx_s + 1, val_t - val_s)
            bit.update(idx_t + 1, val_s - val_t)
        elif tipo == 3:
            l = int(input_data[ptr]); ptr += 1
            r = int(input_data[ptr]); ptr += 1
            results.append(str(query_range(l, r, K, offset_val, P, bit)))
            
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    main()
