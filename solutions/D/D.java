import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class D {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        StringTokenizer st = new StringTokenizer(line);
        if (!st.hasMoreTokens()) return;
        int N = Integer.parseInt(st.nextToken());
        int M = Integer.parseInt(st.nextToken());
        int P = Integer.parseInt(st.nextToken());
        int S = Integer.parseInt(st.nextToken());

        int[] incompat = new int[N];
        for (int i = 0; i < M; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken()) - 1;
            int v = Integer.parseInt(st.nextToken()) - 1;
            incompat[u] |= (1 << v);
            incompat[v] |= (1 << u);
        }

        int bread_mask = (1 << P) - 1;
        int sausage_mask = ((1 << S) - 1) << P;
        long valid_count = 0;

        for (int mask = 0; mask < (1 << N); mask++) {
            if (Integer.bitCount(mask & bread_mask) != 1) continue;
            if (Integer.bitCount(mask & sausage_mask) != 1) continue;

            boolean ok = true;
            for (int i = 0; i < N; i++) {
                if ((mask & (1 << i)) != 0) {
                    if ((mask & incompat[i]) != 0) {
                        ok = false;
                        break;
                    }
                }
            }
            if (ok) {
                valid_count++;
            }
        }
        System.out.println(valid_count);
    }
}
