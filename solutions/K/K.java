import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class K {
    static final int MOD = 998244353;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        StringTokenizer st = new StringTokenizer(line);
        if (!st.hasMoreTokens()) return;
        int N = Integer.parseInt(st.nextToken());
        int K_val = Integer.parseInt(st.nextToken());

        int[] dp = new int[N + 1];
        dp[0] = 1;

        for (int i = 1; i <= N; i++) {
            if (i == K_val) continue;
            for (int j = i; j <= N; j++) {
                dp[j] = (dp[j] + dp[j - i]) % MOD;
            }
        }
        System.out.println(dp[N]);
    }
}
