import sys
import heapq

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(input_data[ptr]); ptr += 1
        v = int(input_data[ptr]); ptr += 1
        c = int(input_data[ptr]); ptr += 1
        adj[u].append((v, c))
        adj[v].append((u, c))
        
    entradas = []
    for _ in range(K):
        entradas.append(int(input_data[ptr])); ptr += 1
        
    INF = 2 * 10**18
    tempo_pessoas = [INF] * (N + 1)
    pq = []
    
    for e in entradas:
        tempo_pessoas[e] = 0
        heapq.heappush(pq, (0, e))
        
    while pq:
        d, u = heapq.heappop(pq)
        if d > tempo_pessoas[u]:
            continue
        for v, w in adj[u]:
            tempo_aresta = 2 * w
            if tempo_pessoas[u] + tempo_aresta < tempo_pessoas[v]:
                tempo_pessoas[v] = tempo_pessoas[u] + tempo_aresta
                heapq.heappush(pq, (tempo_pessoas[v], v))
                
    def testa_caminho(X):
        tempo_carlos = [INF] * (N + 1)
        pq_carlos = []
        if -X <= tempo_pessoas[1]:
            tempo_carlos[1] = -X
            heapq.heappush(pq_carlos, (-X, 1))
        
        while pq_carlos:
            d, u = heapq.heappop(pq_carlos)
            if d > tempo_carlos[u]:
                continue
            if u == N:
                return True
            for v, w in adj[u]:
                tempo_chegada = tempo_carlos[u] + w
                if tempo_chegada <= tempo_pessoas[v] and tempo_chegada < tempo_carlos[v]:
                    tempo_carlos[v] = tempo_chegada
                    heapq.heappush(pq_carlos, (tempo_chegada, v))
        return False

    left = 0
    right = 2 * 10**14
    ans = right
    
    while left <= right:
        mid = (left + right) // 2
        if testa_caminho(mid):
            ans = mid
            right = mid - 1
        else:
            left = mid + 1
            
    print(ans)

if __name__ == "__main__":
    main()
