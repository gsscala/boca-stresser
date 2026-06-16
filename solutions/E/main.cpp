#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Estrutura para os produtos
struct Produto {
    long long x; // Posição
    long long v; // Valor
};

// Comparador para ordenar pela posição
bool comparaPosicao(const Produto& a, const Produto& b) {
    return a.x < b.x;
}

int main() {
    // Otimização de I/O para leitura rápida
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N;
    long long D;
    
    // Lê N e D, encerra se não houver entrada
    if (!(cin >> N >> D)) return 0; 

    vector<Produto> p(N);
    for (int i = 0; i < N; i++) {
        cin >> p[i].x >> p[i].v;
    }

    // 1. Ordenamos os produtos pela posição na rua
    sort(p.begin(), p.end(), comparaPosicao);

    // max_prefix[i] armazenará o maior valor que UM entregador consegue coletar 
    // considerando apenas os produtos do índice 0 até o índice i.
    vector<long long> max_prefix(N, 0);
    long long current_sum = 0;
    int left = 0;

    for (int i = 0; i < N; i++) {
        current_sum += p[i].v;
        
        // Se a distância entre o primeiro item da janela e o atual for > D,
        // removemos os itens da esquerda até que a janela seja válida (<= D).
        while (p[i].x - p[left].x > D) {
            current_sum -= p[left].v;
            left++;
        }
        
        max_prefix[i] = current_sum;
        // Carrega o valor máximo encontrado até o momento
        if (i > 0) {
            max_prefix[i] = max(max_prefix[i], max_prefix[i - 1]);
        }
    }

    // max_suffix[i] armazenará o maior valor que UM entregador consegue coletar 
    // considerando apenas os produtos do índice i até o final (N-1).
    // O tamanho é N+1 para facilitar o cálculo final sem estourar o limite do array.
    vector<long long> max_suffix(N + 1, 0);
    current_sum = 0;
    int right = N - 1;

    for (int i = N - 1; i >= 0; i--) {
        current_sum += p[i].v;
        
        // Se a distância entre o item atual e o último da janela for > D,
        // removemos os itens da direita até a janela voltar a ser válida.
        while (p[right].x - p[i].x > D) {
            current_sum -= p[right].v;
            right--;
        }
        
        max_suffix[i] = current_sum;
        // Carrega o valor máximo olhando do final para o começo
        if (i < N - 1) {
            max_suffix[i] = max(max_suffix[i], max_suffix[i + 1]);
        }
    }

    // 2. A resposta será a combinação máxima de uma janela nos itens à esquerda
    // e outra janela nos itens à direita, sem que elas se sobreponham.
    long long resposta = 0;
    
    for (int i = 0; i < N; i++) {
        // Para qualquer índice i como ponto de divisão:
        // O Entregador 1 pega o melhor intervalo contido em [0...i]
        // O Entregador 2 pega o melhor intervalo contido em [i+1...N-1]
        resposta = max(resposta, max_prefix[i] + max_suffix[i + 1]);
    }

    cout << resposta << "\n";

    return 0;
}
