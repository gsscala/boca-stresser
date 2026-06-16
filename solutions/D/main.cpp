#include <iostream>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N, M, P, S;
    if (!(cin >> N >> M >> P >> S)) return 0;

    // Usaremos um vetor de inteiros onde cada posição guarda a máscara 
    // de incompatibilidade de um ingrediente específico.
    vector<int> incompat(N, 0);
    for (int i = 0; i < M; i++) {
        int u, v;
        cin >> u >> v;
        u--; v--; // Ajustando para índice 0
        incompat[u] |= (1 << v);
        incompat[v] |= (1 << u);
    }

    // Máscaras para identificar facilmente os pães e salsichas
    int bread_mask = (1 << P) - 1; 
    int sausage_mask = ((1 << S) - 1) << P; 
    
    long long valid_count = 0;

    // Testa todas as 2^N combinações possíveis
    for (int mask = 0; mask < (1 << N); mask++) {
        
        // 1. O lanche DEVE ter exatamente 1 pão
        if (__builtin_popcount(mask & bread_mask) != 1) continue;
        
        // 2. O lanche DEVE ter exatamente 1 salsicha
        if (__builtin_popcount(mask & sausage_mask) != 1) continue;

        // 3. Verifica se há ingredientes incompatíveis juntos na máscara atual
        bool ok = true;
        for (int i = 0; i < N; i++) {
            // Se o ingrediente 'i' está no lanche...
            if ((mask & (1 << i))) {
                // ...e algum ingrediente incompatível com 'i' também está: lanche inválido!
                if ((mask & incompat[i]) != 0) {
                    ok = false;
                    break;
                }
            }
        }
        
        if (ok) {
            valid_count++;
        }
    }

    cout << valid_count << "\n";
    return 0;
}
