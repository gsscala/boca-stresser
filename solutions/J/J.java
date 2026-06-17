import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class J {
    static final long MOD = 998244353;
    static final long G = 3;

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

    static void ntt(long[] a, boolean invert) {
        int n = a.length;
        for (int i = 1, j = 0; i < n; i++) {
            int bit = n >> 1;
            for (; (j & bit) != 0; bit >>= 1) j ^= bit;
            j ^= bit;
            if (i < j) {
                long temp = a[i];
                a[i] = a[j];
                a[j] = temp;
            }
        }
        for (int len = 2; len <= n; len <<= 1) {
            long wlen = power(G, (MOD - 1) / len);
            if (invert) wlen = modInverse(wlen);
            for (int i = 0; i < n; i += len) {
                long w = 1;
                for (int j = 0; j < len / 2; j++) {
                    long u = a[i + j];
                    long v = (a[i + j + len / 2] * w) % MOD;
                    a[i + j] = (u + v < MOD ? u + v : u + v - MOD);
                    a[i + j + len / 2] = (u - v >= 0 ? u - v : u - v + MOD);
                    w = (w * wlen) % MOD;
                }
            }
        }
        if (invert) {
            long n_inv = modInverse(n);
            for (int i = 0; i < n; i++) a[i] = (a[i] * n_inv) % MOD;
        }
    }

    static long[] multiply(long[] a, long[] b) {
        if (a.length == 0 || b.length == 0) return new long[0];
        int n = 1;
        while (n < a.length + b.length) n <<= 1;
        long[] fa = Arrays.copyOf(a, n);
        long[] fb = Arrays.copyOf(b, n);
        ntt(fa, false);
        ntt(fb, false);
        for (int i = 0; i < n; i++) fa[i] = (fa[i] * fb[i]) % MOD;
        ntt(fa, true);
        int last = a.length + b.length - 1;
        while (last > 0 && fa[last] == 0) last--;
        return Arrays.copyOf(fa, last + 1);
    }

    static class Result {
        long[] p, q;
        Result(long[] p, long[] q) { this.p = p; this.q = q; }
    }

    static Result compose(long[] P, long[] Q, int l, int r) {
        if (l == r) return new Result(new long[]{P[l]}, Q);
        int mid = l + (r - l) / 2;
        Result left = compose(P, Q, l, mid);
        Result right = compose(P, Q, mid + 1, r);
        long[] rightMult = multiply(left.q, right.p);
        long[] pRes = left.p;
        if (pRes.length < rightMult.length) pRes = Arrays.copyOf(pRes, rightMult.length);
        for (int i = 0; i < rightMult.length; i++) {
            pRes[i] = (pRes[i] + rightMult[i]) % MOD;
        }
        long[] qRes = multiply(left.q, right.q);
        return new Result(pRes, qRes);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int N1 = Integer.parseInt(line.trim());
        long[] P = new long[N1 + 1];
        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 0; i <= N1; i++) P[i] = Long.parseLong(st.nextToken());
        int N2 = Integer.parseInt(br.readLine().trim());
        long[] Q = new long[N2 + 1];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i <= N2; i++) Q[i] = Long.parseLong(st.nextToken());

        long[] res = compose(P, Q, 0, N1).p;
        int target = N1 * N2 + 1;
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < target; i++) {
            sb.append(i < res.length ? res[i] : 0).append(i == target - 1 ? "" : " ");
        }
        System.out.println(sb.toString());
    }
}
