#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    // Otimização de I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N;
    if (!(cin >> N)) return 0;

    // Lendo as N pilhas
    vector<vector<int>> pilhas(N);
    for (int i = 0; i < N; i++) {
        int K;
        cin >> K;
        pilhas[i].resize(K);
        for (int j = 0; j < K; j++) {
            // Os livros são dados da base para o topo
            cin >> pilhas[i][j]; 
        }
    }

    if (N == 1 || N >= 3) {
        // Com 1 ou 3+ pilhas, sempre tem solução
        cout << "S\n";
    } else if (N == 2) {
        // Com 2 pilhas, verificamos o invariante
        vector<int> seq;
        
        // Adicionamos a Pilha 1 de baixo para cima
        for (int x : pilhas[0]) {
            seq.push_back(x);
        }
        
        // Adicionamos a Pilha 2 de cima para baixo (reverso da leitura)
        for (int i = (int)pilhas[1].size() - 1; i >= 0; i--) {
            seq.push_back(pilhas[1][i]);
        }

        // Se a sequência imutável já estiver ordenada, tem solução!
        if (is_sorted(seq.begin(), seq.end())) {
            cout << "S\n";
        } else {
            cout << "N\n";
        }
    }

    return 0;
}
