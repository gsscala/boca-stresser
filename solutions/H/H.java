import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class H {
    static class BIT {
        int size;
        long[] tree;
        BIT(int n) {
            this.size = n;
            this.tree = new long[n + 1];
        }
        void update(int i, long delta) {
            for (; i <= size; i += i & -i) {
                tree[i] += delta;
            }
        }
        long query(int i) {
            long sum = 0;
            for (; i > 0; i -= i & -i) {
                sum += tree[i];
            }
            return sum;
        }
        long query(int l, int r) {
            if (l > r) return 0;
            return query(r) - query(l - 1);
        }
    }

    static long K;
    static long offset_val = 0;
    static long[] P;
    static BIT bit;

    static long sum_block(long B, long L_pos, long R_pos) {
        long len = R_pos - L_pos + 1;
        long base_sum = len * B * K;
        long idx_L = (L_pos + offset_val) % K;
        long idx_R = (R_pos + offset_val) % K;
        long p_sum = 0;
        if (idx_L <= idx_R) {
            p_sum = bit.query((int)idx_L + 1, (int)idx_R + 1);
        } else {
            p_sum = bit.query((int)idx_L + 1, (int)K) + bit.query(1, (int)idx_R + 1);
        }
        return base_sum + p_sum;
    }

    static long query_range(long l, long r) {
        long B_L = l / K;
        long pos_L = l % K;
        long B_R = r / K;
        long pos_R = r % K;

        if (B_L == B_R) {
            return sum_block(B_L, pos_L, pos_R);
        }

        long ans = sum_block(B_L, pos_L, K - 1);
        ans += sum_block(B_R, 0, pos_R);

        if (B_R - B_L > 1) {
            long num = B_R - B_L - 1;
            long A = B_L + 1;
            long B = B_R - 1;
            long p_full = K * (K - 1) / 2;
            ans += num * p_full;
            long A_plus_B = A + B;
            long sum_arithmetic = (A_plus_B * num) / 2;
            long base_full = K * K * sum_arithmetic;
            ans += base_full;
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        StringTokenizer st = new StringTokenizer(line);
        int Q = Integer.parseInt(st.nextToken());
        K = Long.parseLong(st.nextToken());

        P = new long[(int)K];
        bit = new BIT((int)K);
        for (int i = 0; i < (int)K; i++) {
            P[i] = i;
            bit.update(i + 1, i);
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < Q; i++) {
            st = new StringTokenizer(br.readLine());
            int tipo = Integer.parseInt(st.nextToken());
            if (tipo == 1) {
                long p = Long.parseLong(st.nextToken());
                offset_val = (offset_val + p) % K;
            } else if (tipo == 2) {
                long s = Long.parseLong(st.nextToken());
                long t = Long.parseLong(st.nextToken());
                int idx_s = (int)((s + offset_val) % K);
                int idx_t = (int)((t + offset_val) % K);
                long val_s = P[idx_s];
                long val_t = P[idx_t];
                P[idx_s] = val_t;
                P[idx_t] = val_s;
                bit.update(idx_s + 1, val_t - val_s);
                bit.update(idx_t + 1, val_s - val_t);
            } else if (tipo == 3) {
                long l = Long.parseLong(st.nextToken());
                long r = Long.parseLong(st.nextToken());
                sb.append(query_range(l, r)).append("\n");
            }
        }
        System.out.print(sb.toString());
    }
}
