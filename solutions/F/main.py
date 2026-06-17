import sys

# Aumentando o limite de recursão para evitar problemas em árvores profundas
sys.setrecursionlimit(200000)

def dfs(u, pai, profundidade, adj, precisa_resfriar, info):
    subarvore_precisa_resfriar = precisa_resfriar[u]
    if precisa_resfriar[u]:
        info['profundidade_maxima'] = max(info['profundidade_maxima'], profundidade)
        
    for vizinho in adj[u]:
        if vizinho != pai:
            if dfs(vizinho, u, profundidade + 1, adj, precisa_resfriar, info):
                subarvore_precisa_resfriar = True
                info['arestas_subarvore'] += 1
                
    return subarvore_precisa_resfriar

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
    precisa_resfriar = [False] * (N + 1)
    algum_problema = False
    for i in range(1, N + 1):
        temp = int(input_data[ptr]); ptr += 1
        if temp > K:
            precisa_resfriar[i] = True
            algum_problema = True
            
    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u = int(input_data[ptr]); ptr += 1
        v = int(input_data[ptr]); ptr += 1
        adj[u].append(v)
        adj[v].append(u)
        
    if not algum_problema:
        print(0)
        return
        
    info = {'arestas_subarvore': 0, 'profundidade_maxima': 0}
    dfs(1, 0, 0, adj, precisa_resfriar, info)
    
    resposta = (2 * info['arestas_subarvore']) - info['profundidade_maxima']
    print(resposta)

if __name__ == "__main__":
    main()
