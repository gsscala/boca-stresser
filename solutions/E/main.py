import sys

class Produto:
    def __init__(self, x, v):
        self.x = x
        self.v = v

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    D = int(input_data[ptr]); ptr += 1
    
    p = []
    for _ in range(N):
        x = int(input_data[ptr]); ptr += 1
        v = int(input_data[ptr]); ptr += 1
        p.append(Produto(x, v))
        
    p.sort(key=lambda item: item.x)
    
    max_prefix = [0] * N
    current_sum = 0
    left = 0
    for i in range(N):
        current_sum += p[i].v
        while p[i].x - p[left].x > D:
            current_sum -= p[left].v
            left += 1
        max_prefix[i] = current_sum
        if i > 0:
            max_prefix[i] = max(max_prefix[i], max_prefix[i-1])
            
    max_suffix = [0] * (N + 1)
    current_sum = 0
    right = N - 1
    for i in range(N - 1, -1, -1):
        current_sum += p[i].v
        while p[right].x - p[i].x > D:
            current_sum -= p[right].v
            right -= 1
        max_suffix[i] = current_sum
        if i < N - 1:
            max_suffix[i] = max(max_suffix[i], max_suffix[i+1])
            
    resposta = 0
    for i in range(N):
        resposta = max(resposta, max_prefix[i] + max_suffix[i+1])
        
    print(resposta)

if __name__ == "__main__":
    main()
