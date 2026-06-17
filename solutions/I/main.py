import sys

MOD = 998244353

class SAM:
    def __init__(self, s):
        maxlen = len(s)
        self.st = [{'len': 0, 'link': -1, 'next': [-1, -1]} for _ in range(maxlen * 2 + 1)]
        self.sz = 1
        self.last = 0
        for char in s:
            self.extend(0 if char == 'S' else 1)
            
    def extend(self, c):
        cur = self.sz
        self.sz += 1
        self.st[cur]['len'] = self.st[self.last]['len'] + 1
        p = self.last
        while p != -1 and self.st[p]['next'][c] == -1:
            self.st[p]['next'][c] = cur
            p = self.st[p]['link']
        if p == -1:
            self.st[cur]['link'] = 0
        else:
            q = self.st[p]['next'][c]
            if self.st[p]['len'] + 1 == self.st[q]['len']:
                self.st[cur]['link'] = q
            else:
                clone = self.sz
                self.sz += 1
                self.st[clone]['len'] = self.st[p]['len'] + 1
                self.st[clone]['next'] = self.st[q]['next'][:]
                self.st[clone]['link'] = self.st[q]['link']
                while p != -1 and self.st[p]['next'][c] == q:
                    self.st[p]['next'][c] = clone
                    p = self.st[p]['link']
                self.st[q]['link'] = self.st[cur]['link'] = clone
        self.last = cur

def combine(A, B):
    # A, B are tuples: (k, is_full, end_node, end_len, matches)
    is_full = A[1] and B[1]
    k = (A[0] + B[0]) % MOD if A[1] else A[0]
    end_node = B[2]
    if is_full:
        end_len = k
    else:
        end_len = (A[3] + B[0]) % MOD if B[1] else B[3]
    
    extra = B[4]
    if A[1]:
        extra = (extra + B[0] * A[0]) % MOD
    else:
        extra = (extra + B[0] * A[3]) % MOD
    matches = (A[4] + extra) % MOD
    return (k, is_full, end_node, end_len, matches)

def make_char_transition(sam, node, c):
    st = sam.st
    if st[node]['next'][c] != -1:
        return (1, True, st[node]['next'][c], 1, 1)
    else:
        curr = st[node]['link']
        length = 0
        while curr != -1 and st[curr]['next'][c] == -1:
            curr = st[curr]['link']
        if curr != -1:
            length = st[curr]['len']
            curr = st[curr]['next'][c]
            length += 1
        else:
            curr = 0
            length = 0
        return (0, False, curr, length, length)

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    A = input_data[0]
    N = int(input_data[1])
    T_arr = [int(x) for x in input_data[2:]]
    max_T = max(T_arr) if T_arr else 0
    
    sam = SAM(A)
    sz = sam.sz
    
    trans_S = [make_char_transition(sam, i, 0) for i in range(sz)]
    trans_P = [make_char_transition(sam, i, 1) for i in range(sz)]
    
    trans_memo = [None] * (max_T + 1)
    if max_T >= 1:
        trans_memo[1] = [combine(trans_S[i], trans_P[trans_S[i][2]]) for i in range(sz)]
        
    for t in range(2, max_T + 1):
        prev_memo = trans_memo[t-1]
        curr_memo = [None] * sz
        for i in range(sz):
            t1 = trans_S[i]
            t2 = prev_memo[t1[2]]
            t3 = combine(t1, t2)
            t4 = prev_memo[t3[2]]
            curr_memo[i] = combine(t3, t4)
        trans_memo[t] = curr_memo
        
    total_intervals = 0
    curr_node = 0
    curr_len = 0
    for t in T_arr:
        tr = trans_memo[t][curr_node]
        added = (tr[0] * curr_len + tr[4]) % MOD
        total_intervals = (total_intervals + added) % MOD
        if tr[1]:
            curr_len = (curr_len + tr[0]) % MOD
        else:
            curr_len = tr[3]
        curr_node = tr[2]
        
    print(total_intervals)

if __name__ == "__main__":
    main()
