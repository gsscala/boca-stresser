#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const long long MOD = 998244353;
const long long G = 3; // Primitive root for 998244353

// Modular exponentiation
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

long long modInverse(long long n) {
    return power(n, MOD - 2);
}

// Number Theoretic Transform
void ntt(vector<long long>& a, bool invert) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1) j ^= bit;
        j ^= bit;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        long long wlen = power(G, (MOD - 1) / len);
        if (invert) wlen = modInverse(wlen);
        for (int i = 0; i < n; i += len) {
            long long w = 1;
            for (int j = 0; j < len / 2; j++) {
                long long u = a[i + j];
                long long v = (a[i + j + len / 2] * w) % MOD;
                a[i + j] = (u + v < MOD ? u + v : u + v - MOD);
                a[i + j + len / 2] = (u - v >= 0 ? u - v : u - v + MOD);
                w = (w * wlen) % MOD;
            }
        }
    }
    if (invert) {
        long long n_inv = modInverse(n);
        for (long long& x : a) x = (x * n_inv) % MOD;
    }
}

// Polynomial Multiplication using NTT
vector<long long> multiply(const vector<long long>& a, const vector<long long>& b) {
    if (a.empty() || b.empty()) return {};
    vector<long long> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    int n = 1;
    while (n < a.size() + b.size()) n <<= 1;
    fa.resize(n); fb.resize(n);
    
    ntt(fa, false); ntt(fb, false);
    for (int i = 0; i < n; i++) fa[i] = (fa[i] * fb[i]) % MOD;
    ntt(fa, true);
    
    vector<long long> result(a.size() + b.size() - 1);
    for (int i = 0; i < result.size(); i++) result[i] = fa[i];
    while(result.size() > 1 && result.back() == 0) result.pop_back(); // Trim zeros
    return result;
}

// Divide and Conquer Polynomial Composition
pair<vector<long long>, vector<long long>> compose(const vector<long long>& P, const vector<long long>& Q, int l, int r) {
    if (l == r) return {{P[l]}, Q};
    
    int mid = l + (r - l) / 2;
    auto left_res = compose(P, Q, l, mid);
    auto right_res = compose(P, Q, mid + 1, r);
    
    vector<long long> right_mult = multiply(left_res.second, right_res.first);
    
    vector<long long> P_res = left_res.first;
    if (P_res.size() < right_mult.size()) P_res.resize(right_mult.size(), 0);
    for(size_t i = 0; i < right_mult.size(); i++) {
        P_res[i] = (P_res[i] + right_mult[i]) % MOD;
    }
    
    vector<long long> Q_res = multiply(left_res.second, right_res.second);
    return {P_res, Q_res};
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N1, N2;
    if (!(cin >> N1)) return 0;
    vector<long long> P(N1 + 1);
    for (int i = 0; i <= N1; i++) cin >> P[i];

    cin >> N2;
    vector<long long> Q(N2 + 1);
    for (int i = 0; i <= N2; i++) cin >> Q[i];

    // Compute P(Q(x))
    auto res = compose(P, Q, 0, N1).first;
    
    int target = N1 * N2 + 1;
    res.resize(target, 0); 
    
    for (int i = 0; i < target; i++) {
        cout << res[i] << (i == target - 1 ? "" : " ");
    }
    cout << "\n";
    return 0;
}
