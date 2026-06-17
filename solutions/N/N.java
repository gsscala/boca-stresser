import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class N {
    static final int MAX_D = 1000000;
    static final int MAX_N = 100000;

    static int[] count_K = new int[MAX_D + 1];
    static int[] freq = new int[MAX_N + 1];
    static boolean[] is_lit = new boolean[MAX_D + 1];
    static int current_max = 0;

    static void add_count(int K) {
        int old_val = count_K[K];
        freq[old_val]--;
        count_K[K]++;
        int new_val = count_K[K];
        freq[new_val]++;
        if (new_val > current_max) {
            current_max = new_val;
        }
    }

    static void remove_count(int K) {
        int old_val = count_K[K];
        freq[old_val]--;
        count_K[K]--;
        int new_val = count_K[K];
        freq[new_val]++;
        if (current_max == old_val && freq[old_val] == 0) {
            current_max--;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int n_ops = Integer.parseInt(line.trim());
        freq[0] = MAX_D - 1;

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n_ops; i++) {
            line = br.readLine();
            if (line == null) break;
            int D = Integer.parseInt(line.trim());

            List<Integer> divisores = new ArrayList<>();
            for (int d = 1; d * d <= D; d++) {
                if (D % d == 0) {
                    if (d > 1) divisores.add(d);
                    int outro = D / d;
                    if (outro != d && outro > 1) {
                        divisores.add(outro);
                    }
                }
            }

            if (is_lit[D]) {
                is_lit[D] = false;
                for (int k : divisores) remove_count(k);
            } else {
                is_lit[D] = true;
                for (int k : divisores) add_count(k);
            }
            sb.append(current_max).append("\n");
        }
        System.out.print(sb.toString());
    }
}
