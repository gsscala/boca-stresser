#include <iostream>
#include <vector>
#include <queue>

using namespace std;

const long long INF = 1e18; // Infinito seguro para evitar overflow

struct Edge {
    int to;
    long long weight;
};

int main() {
    // Otimização de I/O para maratona
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N, M, K;
    if (!(cin >> N >> M >> K)) return 0;

    vector<vector<Edge>> adj(N + 1);
    for (int i = 0; i < M; i++) {
        int u, v;
        long long c;
        cin >> u >> v >> c;
        // Grafo não-direcionado
        adj[u].push_back({v, c});
        adj[v].push_back({u, c});
    }

    vector<int> entradas(K);
    for (int i = 0; i < K; i++) {
        cin >> entradas[i];
    }

    // ========================================================
    // PASSO 1: Dijkstra Multi-fonte para as pessoas
    // ========================================================
    vector<long long> tempo_pessoas(N + 1, INF);
    // priority_queue armazenando {tempo, vertice}
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq_pessoas;

    // Todas as entradas começam no tempo 0
    for (int e : entradas) {
        tempo_pessoas[e] = 0;
        pq_pessoas.push({0, e});
    }

    while (!pq_pessoas.empty()) {
        auto [tempo_atual, u] = pq_pessoas.top();
        pq_pessoas.pop();

        if (tempo_atual > tempo_pessoas[u]) continue;

        for (const auto& edge : adj[u]) {
            // Pessoas levam 2*D de tempo
            long long tempo_aresta = 2LL * edge.weight; 
            if (tempo_pessoas[u] + tempo_aresta < tempo_pessoas[edge.to]) {
                tempo_pessoas[edge.to] = tempo_pessoas[u] + tempo_aresta;
                pq_pessoas.push({tempo_pessoas[edge.to], edge.to});
            }
        }
    }

    // ========================================================
    // PASSO 2: Busca Binária para o tempo de antecedência de Carlos
    // ========================================================
    long long left = 0;
    long long right = 2e14; // Limite superior arbitrariamente grande e seguro
    long long ans = right;

    // Função que verifica se Carlos consegue chegar no vértice N com antecedência X
    auto testa_caminho = [&](long long X) {
        vector<long long> tempo_carlos(N + 1, INF);
        priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq_carlos;

        // Carlos sai do vértice 1 no tempo -X. Ele só pode sair se não tiver gente lá.
        if (-X <= tempo_pessoas[1]) {
            tempo_carlos[1] = -X;
            pq_carlos.push({-X, 1});
        }

        while (!pq_carlos.empty()) {
            auto [tempo_atual, u] = pq_carlos.top();
            pq_carlos.pop();

            if (tempo_atual > tempo_carlos[u]) continue;
            
            // Se chegou no destino, o tempo X é suficiente
            if (u == N) return true;

            for (const auto& edge : adj[u]) {
                // Carlos leva 1*D de tempo
                long long tempo_chegada = tempo_carlos[u] + edge.weight; 
                
                // Só pode passar se chegar antes ou no mesmo instante que as pessoas
                if (tempo_chegada <= tempo_pessoas[edge.to] && tempo_chegada < tempo_carlos[edge.to]) {
                    tempo_carlos[edge.to] = tempo_chegada;
                    pq_carlos.push({tempo_chegada, edge.to});
                }
            }
        }

        // Se a fila esvaziou e não retornou true, o caminho não é possível com esse X
        return false;
    };

    while (left <= right) {
        long long mid = left + (right - left) / 2;
        
        if (testa_caminho(mid)) {
            ans = mid;         // Salvamos a resposta válida
            right = mid - 1;   // Tentamos achar um tempo de antecedência ainda menor
        } else {
            left = mid + 1;    // Falhou, precisa de mais antecedência
        }
    }

    cout << ans << "\n";

    return 0;
}
