import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    
    if N == 1 or N >= 3:
        print("S")
        return
        
    pilhas = []
    for _ in range(N):
        K = int(input_data[ptr]); ptr += 1
        curr_p = []
        for _ in range(K):
            curr_p.append(int(input_data[ptr])); ptr += 1
        pilhas.append(curr_p)
        
    if N == 2:
        seq = []
        for x in pilhas[0]:
            seq.append(x)
        for i in range(len(pilhas[1]) - 1, -1, -1):
            seq.append(pilhas[1][i])
            
        if all(seq[i] <= seq[i+1] for i in range(len(seq)-1)):
            print("S")
        else:
            print("N")

if __name__ == "__main__":
    main()
