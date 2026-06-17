import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class L {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        int N = Integer.parseInt(line.trim());

        if (N == 1 || N >= 3) {
            System.out.println("S");
            return;
        }

        List<Integer>[] pilhas = new ArrayList[N];
        for (int i = 0; i < N; i++) {
            pilhas[i] = new ArrayList<>();
            StringTokenizer st = new StringTokenizer(br.readLine());
            int K = Integer.parseInt(st.nextToken());
            for (int j = 0; j < K; j++) {
                pilhas[i].add(Integer.parseInt(st.nextToken()));
            }
        }

        if (N == 2) {
            List<Integer> seq = new ArrayList<>();
            for (int x : pilhas[0]) {
                seq.add(x);
            }
            for (int i = pilhas[1].size() - 1; i >= 0; i--) {
                seq.add(pilhas[1].get(i));
            }

            boolean sorted = true;
            for (int i = 0; i < seq.size() - 1; i++) {
                if (seq.get(i) > seq.get(i + 1)) {
                    sorted = false;
                    break;
                }
            }
            if (sorted) {
                System.out.println("S");
            } else {
                System.out.println("N");
            }
        }
    }
}
