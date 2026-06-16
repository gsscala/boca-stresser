#include <iostream>
#include <vector>

using namespace std;

const int MOD = 998244353;

int main() {
    // Otimização de I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N, K;
    if (!(cin >> N >> K)) return 0;

    // dp[j] armazena o número de maneiras de obter a soma de 'j' chutes
    vector<int> dp(N + 1, 0);
    
    // Caso base: 1 maneira de ter 0 chutes (fazer nada)
    dp[0] = 1;

    // Iteramos por todos os tamanhos de séries possíveis (os 'pesos' da nossa DP)
    for (int i = 1; i <= N; i++) {
        // Ignoramos a série de tamanho K, pois Matheus a acha sem graça
        if (i == K) continue;

        // Atualizamos as somas possíveis se decidirmos usar séries de tamanho 'i'
        for (int j = i; j <= N; j++) {
            dp[j] = (dp[j] + dp[j - i]) % MOD;
        }
    }

    // A resposta final é o número de maneiras de somar exatamente N
    cout << dp[N] << "\n";

    return 0;
}
