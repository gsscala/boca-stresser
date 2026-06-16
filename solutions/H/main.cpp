#include <iostream>
#include <vector>

using namespace std;

// Fenwick Tree (BIT) para manter a soma dinâmica do bloco de tamanho K
struct BIT {
    int size;
    vector<long long> tree;

    BIT(int n) {
        size = n;
        tree.assign(n + 1, 0);
    }

    void update(int i, long long delta) {
        for (; i <= size; i += i & -i) {
            tree[i] += delta;
        }
    }

    long long query(int i) {
        long long sum = 0;
        for (; i > 0; i -= i & -i) {
            sum += tree[i];
        }
        return sum;
    }

    long long query(int l, int r) {
        if (l > r) return 0;
        return query(r) - query(l - 1);
    }
};

long long K;
long long offset_val = 0;
vector<long long> P;
BIT* bit;

// Função que calcula a soma de um pedaço específico de um bloco
long long sum_block(long long B, long long L_pos, long long R_pos) {
    long long len = R_pos - L_pos + 1;
    long long base_sum = len * B * K;

    // Converte as posições atuais paras as posições originais afetadas pelo offset
    long long idx_L = (L_pos + offset_val) % K;
    long long idx_R = (R_pos + offset_val) % K;

    long long p_sum = 0;
    
    // Se o intervalo de índices originais for contínuo, fazemos uma consulta.
    // Se "der a volta" no array (devido ao offset), separamos em duas consultas.
    if (idx_L <= idx_R) {
        p_sum = bit->query(idx_L + 1, idx_R + 1); // BIT é 1-indexada
    } else {
        p_sum = bit->query(idx_L + 1, K) + bit->query(1, idx_R + 1);
    }

    return base_sum + p_sum;
}

// Função que processa a consulta tipo 3 (L até R global)
long long query_range(long long l, long long r) {
    long long B_L = l / K;
    long long pos_L = l % K;
    long long B_R = r / K;
    long long pos_R = r % K;

    // Se tudo estiver dentro do mesmo bloco
    if (B_L == B_R) {
        return sum_block(B_L, pos_L, pos_R);
    }

    // Calcula o pedaço do bloco da esquerda e o pedaço do bloco da direita
    long long ans = sum_block(B_L, pos_L, K - 1);
    ans += sum_block(B_R, 0, pos_R);

    // Se houver blocos inteiros no meio, usa matemática pura O(1)
    if (B_R - B_L > 1) {
        long long num = B_R - B_L - 1;
        long long A = B_L + 1;
        long long B = B_R - 1;

        // A soma dos elementos base (de 0 a K-1) que compõem o bloco
        unsigned long long p_full = (unsigned long long)K * (K - 1) / 2;
        ans += num * p_full;

        // A soma dos multiplicadores dos blocos (PA)
        unsigned long long A_plus_B = A + B;
        unsigned long long sum_arithmetic = (A_plus_B * num) / 2;
        unsigned long long base_full = (unsigned long long)K * K * sum_arithmetic;
        ans += base_full;
    }

    return ans;
}

int main() {
    // Otimização severa de I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int Q;
    if (!(cin >> Q >> K)) return 0;

    // Inicialização
    P.assign(K, 0);
    bit = new BIT(K);

    for (int i = 0; i < K; i++) {
        P[i] = i;
        bit->update(i + 1, i);
    }

    // Processamento das operações
    for (int i = 0; i < Q; i++) {
        int tipo;
        cin >> tipo;

        if (tipo == 1) {
            long long p;
            cin >> p;
            offset_val = (offset_val + p) % K;
            
        } else if (tipo == 2) {
            long long s, t;
            cin >> s >> t;
            
            // Acha os índices reais no array P
            int idx_s = (s + offset_val) % K;
            int idx_t = (t + offset_val) % K;

            long long val_s = P[idx_s];
            long long val_t = P[idx_t];

            // Atualiza os valores no array base
            P[idx_s] = val_t;
            P[idx_t] = val_s;

            // Atualiza na BIT
            bit->update(idx_s + 1, val_t - val_s);
            bit->update(idx_t + 1, val_s - val_t);
            
        } else if (tipo == 3) {
            long long l, r;
            cin >> l >> r;
            cout << query_range(l, r) << "\n";
        }
    }

    delete bit;
    return 0;
}
