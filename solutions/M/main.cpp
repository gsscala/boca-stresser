#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const long long MOD = 998244353;

// Exponenciação modular para calcular o inverso
long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

// Inverso modular usando o Pequeno Teorema de Fermat
long long modInverse(long long n) {
    return power(n, MOD - 2);
}

// SegTree para manter o produto dinâmico das opções (Frequência + 1)
struct SegTree {
    int n;
    vector<long long> tree;
    SegTree(int n) : n(n), tree(4 * n + 1, 1) {}

    void update(int node, int start, int end, int idx, long long val) {
        if (start == end) {
            tree[node] = val % MOD;
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = (tree[2 * node] * tree[2 * node + 1]) % MOD;
    }

    long long query(int node, int start, int end, int l, int r) {
        if (r < start || end < l || l > r) return 1; // Elemento neutro da multiplicação
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        long long p1 = query(2 * node, start, mid, l, r);
        long long p2 = query(2 * node + 1, mid + 1, end, l, r);
        return (p1 * p2) % MOD;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N, K;
    if (!(cin >> N >> K)) return 0;

    vector<int> T(N + 1);
    vector<vector<int>> occ(N + 1);
    vector<int> last(N + 1, 0);

    // Lemos os dados e guardamos a última ocorrência de cada tipo
    for (int i = 1; i <= N; i++) {
        cin >> T[i];
        occ[T[i]].push_back(i);
        last[T[i]] = i; // Atualiza para a ocorrência mais à direita
    }

    SegTree st(N);
    vector<long long> C(N + 1, 0); // Frequência de cada tipo no intervalo sobrevivente
    int pool_end = 0;
    long long ans = 0;

    for (int j = 1; j <= N; j++) {
        // Expandimos a janela de sobreviventes
        int max_pool = max(0, j - K - 1);
        while (pool_end < max_pool) {
            pool_end++;
            int type = T[pool_end];
            C[type]++;
            // Atualizamos a SegTree na posição final do tipo
            st.update(1, 1, N, last[type], C[type] + 1);
        }

        // Só processamos conjuntos ancorados na ÚLTIMA ocorrência do tipo T[j]
        // Isso evita qualquer contagem duplicada matematicamente.
        if (j == last[T[j]]) {
            int search_val = max(1, j - K);
            // Encontra a primeira vez que a concha j aparece cobrindo o impacto
            auto it = lower_bound(occ[T[j]].begin(), occ[T[j]].end(), search_val);
            int pos = *it;
            int limit = pos + K + 1;

            long long waysA = 0;
            if (C[T[j]] > 0) {
                long long prodA = st.query(1, 1, N, 1, j - 1);
                waysA = (C[T[j]] * prodA) % MOD;
            }

            int query_limit = min(N, limit - 1);
            long long prodB_full = st.query(1, 1, N, 1, query_limit);
            
            // Removemos a contribuição do próprio elemento âncora da multiplicação
            long long waysB = (prodB_full * modInverse(C[T[j]] + 1)) % MOD;

            ans = (ans + waysA + waysB) % MOD;
        }
    }

    cout << ans << "\n";
    return 0;
}
