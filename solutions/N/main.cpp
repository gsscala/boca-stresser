#include <iostream>
#include <vector>

using namespace std;

// Limites dados no problema
const int MAX_D = 1000000;
const int MAX_N = 100000;

// Variáveis globais (já inicializadas com 0/false por padrão no C++)
int count_K[MAX_D + 1]; // count_K[i] = qtd de degraus acesos múltiplos de i
int freq[MAX_N + 1];    // freq[i] = qtd de "K"s que possuem exatamente 'i' degraus acesos
bool is_lit[MAX_D + 1]; // Estado da luz do degrau (true = acesa, false = apagada)

int current_max = 0; // Guarda a resposta global atual

// Função para adicionar um múltiplo à contagem de K
void add_count(int K) {
    int old_val = count_K[K];
    freq[old_val]--; // Remove da frequência antiga
    
    count_K[K]++;
    
    int new_val = count_K[K];
    freq[new_val]++; // Adiciona na nova frequência
    
    // Atualiza o máximo global se necessário
    if (new_val > current_max) {
        current_max = new_val;
    }
}

// Função para remover um múltiplo da contagem de K
void remove_count(int K) {
    int old_val = count_K[K];
    freq[old_val]--;
    
    count_K[K]--;
    
    int new_val = count_K[K];
    freq[new_val]++;
    
    // Se o valor que abaixou era o máximo único absoluto, o máximo também abaixa
    if (current_max == old_val && freq[old_val] == 0) {
        current_max--;
    }
}

int main() {
    // Otimização essencial de I/O para maratona
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N;
    if (!(cin >> N)) return 0;

    // Inicialmente, todos os 'K' possuem 0 luzes acesas
    // Como K vai de 2 até MAX_D, temos MAX_D - 1 valores possíveis para K
    freq[0] = MAX_D - 1;

    for (int i = 0; i < N; i++) {
        int D;
        cin >> D;

        // Encontra todos os divisores de D em O(sqrt(D))
        vector<int> divisores;
        for (int d = 1; d * d <= D; d++) {
            if (D % d == 0) {
                if (d > 1) divisores.push_back(d); // K sempre > 1
                
                int outro_divisor = D / d;
                // Evita adicionar duas vezes se for quadrado perfeito e garante K > 1
                if (outro_divisor != d && outro_divisor > 1) {
                    divisores.push_back(outro_divisor);
                }
            }
        }

        // Se o degrau estiver aceso, apagamos. Se estiver apagado, acendemos.
        if (is_lit[D]) {
            is_lit[D] = false;
            for (int k : divisores) {
                remove_count(k);
            }
        } else {
            is_lit[D] = true;
            for (int k : divisores) {
                add_count(k);
            }
        }

        // A resposta após a operação é o nosso máximo atual
        cout << current_max << "\n";
    }

    return 0;
}
