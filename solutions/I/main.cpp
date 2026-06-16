#include <iostream>
#include <vector>
#include <string>

using namespace std;

const long long MOD = 998244353;

// Estrutura clássica do Suffix Automaton
struct State {
    int len, link;
    int next[2]; // 'S' -> 0, 'P' -> 1
};

const int MAXLEN = 1005;
State st[MAXLEN * 2];
int sz, last;

void sam_init() {
    st[0].len = 0;
    st[0].link = -1;
    st[0].next[0] = st[0].next[1] = -1;
    sz = 1;
    last = 0;
}

void sam_extend(int c) {
    int cur = sz++;
    st[cur].len = st[last].len + 1;
    st[cur].next[0] = st[cur].next[1] = -1;
    
    int p = last;
    while (p != -1 && st[p].next[c] == -1) {
        st[p].next[c] = cur;
        p = st[p].link;
    }
    if (p == -1) {
        st[cur].link = 0;
    } else {
        int q = st[p].next[c];
        if (st[p].len + 1 == st[q].len) {
            st[cur].link = q;
        } else {
            int clone = sz++;
            st[clone].len = st[p].len + 1;
            st[clone].next[0] = st[q].next[0];
            st[clone].next[1] = st[q].next[1];
            st[clone].link = st[q].link;
            while (p != -1 && st[p].next[c] == q) {
                st[p].next[c] = clone;
                p = st[p].link;
            }
            st[q].link = st[cur].link = clone;
        }
    }
    last = cur;
}

// Representa o efeito matemático de passar uma string inteira pelo SAM
struct Transition {
    long long k;       // Coeficiente de dependência do len inicial
    bool is_full;      // Verdadeiro se a string NUNCA seguiu um link (match perfeito)
    int end_node;      // Nó do SAM onde a string termina
    long long end_len; // Se is_full for falso, este é o len final exato
    long long matches; // Parte constante dos matches adicionados
};

// Combina duas transições A e B (Processar string A seguida da string B) em O(1)
Transition combine(const Transition& A, const Transition& B) {
    Transition C;
    C.is_full = A.is_full && B.is_full;
    C.k = (A.is_full ? A.k + B.k : A.k) % MOD;
    C.end_node = B.end_node;
    
    if (C.is_full) {
        C.end_len = C.k; 
    } else {
        if (B.is_full) {
            C.end_len = (A.end_len + B.k) % MOD;
        } else {
            C.end_len = B.end_len;
        }
    }
    
    // Calcula as novas combinações (matches) geradas matematicamente
    long long extra = B.matches;
    if (A.is_full) {
        extra = (extra + B.k * A.k) % MOD;
    } else {
        extra = (extra + B.k * A.end_len) % MOD;
    }
    C.matches = (A.matches + extra) % MOD;
    
    return C;
}

// Cria a transição base para processar um único caractere
Transition make_char_transition(int node, char ch) {
    int c = (ch == 'S') ? 0 : 1;
    Transition T;
    
    if (st[node].next[c] != -1) {
        // Caractere casou perfeitamente
        T.is_full = true;
        T.k = 1;
        T.end_node = st[node].next[c];
        T.end_len = 1;
        T.matches = 1;
    } else {
        // Caractere falhou, precisa seguir links de fallback
        T.is_full = false;
        T.k = 0;
        int curr = st[node].link;
        int len = 0;
        while (curr != -1 && st[curr].next[c] == -1) {
            curr = st[curr].link;
        }
        if (curr != -1) {
            len = st[curr].len;
            curr = st[curr].next[c];
            len++;
        } else {
            curr = 0;
            len = 0;
        }
        T.end_node = curr;
        T.end_len = len;
        T.matches = len; // Novo comprimento absoluto
    }
    return T;
}

// Matrizes globais para evitar estouro de pilha
Transition trans_memo[1005][2005];
Transition trans_S[2005];
Transition trans_P[2005];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    string A;
    if (!(cin >> A)) return 0;

    int N;
    cin >> N;
    vector<int> T(N);
    int max_T = 0;
    for (int i = 0; i < N; i++) {
        cin >> T[i];
        if (T[i] > max_T) max_T = T[i];
    }

    sam_init();
    for (char c : A) {
        sam_extend(c == 'S' ? 0 : 1);
    }

    // 1. Pré-calcula transições básicas dos caracteres S e P para todo nó possível
    for (int i = 0; i < sz; i++) {
        trans_S[i] = make_char_transition(i, 'S');
        trans_P[i] = make_char_transition(i, 'P');
    }

    // 2. Constrói o caso base (s1 = SP)
    if (max_T >= 1) {
        for (int i = 0; i < sz; i++) {
            trans_memo[1][i] = combine(trans_S[i], trans_P[trans_S[i].end_node]);
        }
    }

    // 3. Monta todos os s_t necessários de forma recursiva: s_t = S + s_{t-1} + s_{t-1}
    for (int t = 2; t <= max_T; t++) {
        for (int i = 0; i < sz; i++) {
            Transition t1 = trans_S[i]; 
            Transition t2 = trans_memo[t - 1][t1.end_node];
            Transition t3 = combine(t1, t2); // t3 = S + s_{t-1}
            Transition t4 = trans_memo[t - 1][t3.end_node];
            
            trans_memo[t][i] = combine(t3, t4); // s_t concluído
        }
    }

    // 4. Resolve a String B usando os blocos gigantes já matematicamente calculados
    long long total_intervals = 0;
    int curr_node = 0;
    long long curr_len = 0;

    for (int i = 0; i < N; i++) {
        int t = T[i];
        Transition tr = trans_memo[t][curr_node];
        
        // Aplica a equação linear que descobre os matches!
        long long added = (tr.k * curr_len + tr.matches) % MOD;
        total_intervals = (total_intervals + added) % MOD;
        
        // Atualiza a herança (o "len") para o próximo bloco
        if (tr.is_full) {
            curr_len = (curr_len + tr.k) % MOD;
        } else {
            curr_len = tr.end_len;
        }
        curr_node = tr.end_node;
    }

    cout << total_intervals << "\n";
    return 0;
}
