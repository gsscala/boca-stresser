import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    P = int(input_data[ptr]); ptr += 1
    S = int(input_data[ptr]); ptr += 1
    
    incompat = [0] * N
    for _ in range(M):
        u = int(input_data[ptr]) - 1; ptr += 1
        v = int(input_data[ptr]) - 1; ptr += 1
        incompat[u] |= (1 << v)
        incompat[v] |= (1 << u)
        
    bread_mask = (1 << P) - 1
    sausage_mask = ((1 << S) - 1) << P
    valid_count = 0
    
    for mask in range(1 << N):
        if bin(mask & bread_mask).count('1') != 1:
            continue
        if bin(mask & sausage_mask).count('1') != 1:
            continue
            
        ok = True
        for i in range(N):
            if (mask & (1 << i)):
                if (mask & incompat[i]):
                    ok = False
                    break
        if ok:
            valid_count += 1
            
    print(valid_count)

if __name__ == "__main__":
    main()
