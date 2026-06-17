import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])
    
    MOD = 998244353
    dp = [0] * (N + 1)
    dp[0] = 1
    
    for i in range(1, N + 1):
        if i == K:
            continue
        for j in range(i, N + 1):
            dp[j] = (dp[j] + dp[j - i]) % MOD
            
    print(dp[N])

if __name__ == "__main__":
    main()
