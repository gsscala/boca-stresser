#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Variáveis globais para facilitar a DFS
vector<vector<int>> adj;
vector<bool> precisa_resfriar;
int K;
long long arestas_subarvore = 0; // Nosso 'E'
int profundidade_maxima = 0;     // Nosso 'L'

// DFS que retorna true se a subárvore a partir de 'u' contém algum cômodo problemático
bool dfs(int u, int pai, int profundidade) {
    // Verifica se o cômodo atual precisa de resfriamento
    bool subarvore_precisa_resfriar = precisa_resfriar[u];
    
    if (precisa_resfriar[u]) {
        profundidade_maxima = max(profundidade_maxima, profundidade);
    }

    // Explora os vizinhos (filhos na árvore)
    for (int vizinho : adj[u]) {
        if (vizinho != pai) {
            // Se o filho (ou alguém abaixo dele) precisa de resfriamento
            if (dfs(vizinho, u, profundidade + 1)) {
                subarvore_precisa_resfriar = true;
                arestas_subarvore++; // Esta aresta fará parte do caminho do Newto
            }
        }
    }
    
    return subarvore_precisa_resfriar;
}

int main() {
    // Otimização de I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N;
    if (!(cin >> N >> K)) return 0;

    adj.resize(N + 1);
    precisa_resfriar.assign(N + 1, false);

    bool algum_problema = false;

    // Lendo as temperaturas
    for (int i = 1; i <= N; i++) {
        int temp;
        cin >> temp;
        if (temp > K) {
            precisa_resfriar[i] = true;
            algum_problema = true;
        }
    }

    // Lendo as conexões (N-1 corredores)
    for (int i = 0; i < N - 1; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    // Se nenhum cômodo passa de K, ele não precisa andar nada
    if (!algum_problema) {
        cout << 0 << "\n";
        return 0;
    }

    // Inicia a DFS a partir da sala 1 (raiz), que tem pai 0 e profundidade 0
    dfs(1, 0, 0);

    // O cálculo mágico: vai e volta em todas as arestas úteis, 
    // menos a volta do caminho mais longo
    int resposta = (2 * arestas_subarvore) - profundidade_maxima;

    cout << resposta << "\n";

    return 0;
}
