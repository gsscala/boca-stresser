import sys

MAX_D = 1000000
MAX_N = 100000

count_K = [0] * (MAX_D + 1)
freq = [0] * (MAX_N + 1)
is_lit = [False] * (MAX_D + 1)
current_max = 0

def add_count(K):
    global current_max
    old_val = count_K[K]
    freq[old_val] -= 1
    count_K[K] += 1
    new_val = count_K[K]
    freq[new_val] += 1
    if new_val > current_max:
        current_max = new_val

def remove_count(K):
    global current_max
    old_val = count_K[K]
    freq[old_val] -= 1
    count_K[K] -= 1
    new_val = count_K[K]
    freq[new_val] += 1
    if current_max == old_val and freq[old_val] == 0:
        current_max -= 1

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N_ops = int(input_data[0])
    freq[0] = MAX_D - 1
    
    results = []
    for i in range(1, N_ops + 1):
        D = int(input_data[i])
        
        divisores = []
        d = 1
        while d * d <= D:
            if D % d == 0:
                if d > 1:
                    divisores.append(d)
                outro = D // d
                if outro != d and outro > 1:
                    divisores.append(outro)
            d += 1
            
        if is_lit[D]:
            is_lit[D] = False
            for k in divisores:
                remove_count(k)
        else:
            is_lit[D] = True
            for k in divisores:
                add_count(k)
        results.append(str(current_max))
        
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    main()
