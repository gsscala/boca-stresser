import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.StringTokenizer;

public class E {
    static class Produto implements Comparable<Produto> {
        long x, v;
        Produto(long x, long v) {
            this.x = x;
            this.v = v;
        }
        @Override
        public int compareTo(Produto other) {
            return Long.compare(this.x, other.x);
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        StringTokenizer st = new StringTokenizer(line);
        if (!st.hasMoreTokens()) return;
        int N = Integer.parseInt(st.nextToken());
        long D = Long.parseLong(st.nextToken());

        Produto[] p = new Produto[N];
        for (int i = 0; i < N; i++) {
            st = new StringTokenizer(br.readLine());
            p[i] = new Produto(Long.parseLong(st.nextToken()), Long.parseLong(st.nextToken()));
        }

        Arrays.sort(p);

        long[] max_prefix = new long[N];
        long current_sum = 0;
        int left = 0;
        for (int i = 0; i < N; i++) {
            current_sum += p[i].v;
            while (p[i].x - p[left].x > D) {
                current_sum -= p[left].v;
                left++;
            }
            max_prefix[i] = current_sum;
            if (i > 0) {
                max_prefix[i] = Math.max(max_prefix[i], max_prefix[i - 1]);
            }
        }

        long[] max_suffix = new long[N + 1];
        current_sum = 0;
        int right = N - 1;
        for (int i = N - 1; i >= 0; i--) {
            current_sum += p[i].v;
            while (p[right].x - p[i].x > D) {
                current_sum -= p[right].v;
                right--;
            }
            max_suffix[i] = current_sum;
            if (i < N - 1) {
                max_suffix[i] = Math.max(max_suffix[i], max_suffix[i + 1]);
            }
        }

        long resposta = 0;
        for (int i = 0; i < N; i++) {
            resposta = Math.max(resposta, max_prefix[i] + max_suffix[i + 1]);
        }
        System.out.println(resposta);
    }
}
