import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class M {
    static final long MOD = 998244353;

    static long power(long base, long exp) {
        long res = 1;
        base %= MOD;
        while (exp > 0) {
            if (exp % 2 == 1) res = (res * base) % MOD;
            base = (base * base) % MOD;
            exp /= 2;
        }
        return res;
    }

    static long modInverse(long n) {
        return power(n, MOD - 2);
    }

    static class SegTree {
        int n;
        long[] tree;
        SegTree(int n) {
            this.n = n;
            tree = new long[4 * n + 1];
            Arrays.fill(tree, 1);
        }
        void update(int node, int start, int end, int idx, long val) {
            if (start == end) {
                tree[node] = val % MOD;
                return;
            }
            int mid = (start + end) / 2;
            if (idx <= mid) update(2 * node, start, mid, idx, val);
            else update(2 * node + 1, mid + 1, end, idx, val);
            tree[node] = (tree[2 * node] * tree[2 * node + 1]) % MOD;
        }
        long query(int node, int start, int end, int l, int r) {
            if (r < start || end < l || l > r) return 1;
            if (l <= start && end <= r) return tree[node];
            int mid = (start + end) / 2;
            long p1 = query(2 * node, start, mid, l, r);
            long p2 = query(2 * node + 1, mid + 1, end, l, r);
            return (p1 * p2) % MOD;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        StringTokenizer stTok = new StringTokenizer(line);
        int N = Integer.parseInt(stTok.nextToken());
        int K = Integer.parseInt(stTok.nextToken());

        int[] T = new int[N + 1];
        List<Integer>[] occ = new ArrayList[N + 1];
        for (int i = 0; i <= N; i++) occ[i] = new ArrayList<>();
        int[] last = new int[N + 1];

        line = br.readLine();
        if (line != null) {
            stTok = new StringTokenizer(line);
            for (int i = 1; i <= N; i++) {
                T[i] = Integer.parseInt(stTok.nextToken());
                occ[T[i]].add(i);
                last[T[i]] = i;
            }
        }

        SegTree st = new SegTree(N);
        long[] C = new long[N + 1];
        int pool_end = 0;
        long ans = 0;

        for (int j = 1; j <= N; j++) {
            int max_pool = Math.max(0, j - K - 1);
            while (pool_end < max_pool) {
                pool_end++;
                int type = T[pool_end];
                C[type]++;
                st.update(1, 1, N, last[type], C[type] + 1);
            }

            if (j == last[T[j]]) {
                int search_val = Math.max(1, j - K);
                List<Integer> list = occ[T[j]];
                int pos_idx = Collections.binarySearch(list, search_val);
                if (pos_idx < 0) pos_idx = -(pos_idx + 1);
                int pos = list.get(pos_idx);
                int limit = pos + K + 1;

                long waysA = 0;
                if (C[T[j]] > 0) {
                    long prodA = st.query(1, 1, N, 1, j - 1);
                    waysA = (C[T[j]] * prodA) % MOD;
                }

                int query_limit = Math.min(N, limit - 1);
                long prodB_full = st.query(1, 1, N, 1, query_limit);
                long waysB = (prodB_full * modInverse(C[T[j]] + 1)) % MOD;

                ans = (ans + waysA + waysB) % MOD;
            }
        }
        System.out.println(ans);
    }
}
