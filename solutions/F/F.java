import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class F {
    static List<Integer>[] adj;
    static boolean[] precisa_resfriar;
    static long arestas_subarvore = 0;
    static int profundidade_maxima = 0;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        StringTokenizer st = new StringTokenizer(line);
        int N = Integer.parseInt(st.nextToken());
        int K = Integer.parseInt(st.nextToken());

        precisa_resfriar = new boolean[N + 1];
        boolean algum_problema = false;
        st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= N; i++) {
            int temp = Integer.parseInt(st.nextToken());
            if (temp > K) {
                precisa_resfriar[i] = true;
                algum_problema = true;
            }
        }

        adj = new ArrayList[N + 1];
        for (int i = 1; i <= N; i++) adj[i] = new ArrayList<>();

        for (int i = 0; i < N - 1; i++) {
            line = br.readLine();
            if (line == null) break;
            st = new StringTokenizer(line);
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            adj[u].add(v);
            adj[v].add(u);
        }

        if (!algum_problema) {
            System.out.println(0);
            return;
        }

        dfs(1, 0, 0);

        long resposta = (2 * arestas_subarvore) - profundidade_maxima;
        System.out.println(resposta);
    }

    static boolean dfs(int u, int pai, int profundidade) {
        boolean subarvore_precisa_resfriar = precisa_resfriar[u];
        if (precisa_resfriar[u]) {
            profundidade_maxima = Math.max(profundidade_maxima, profundidade);
        }

        for (int vizinho : adj[u]) {
            if (vizinho != pai) {
                if (dfs(vizinho, u, profundidade + 1)) {
                    subarvore_precisa_resfriar = true;
                    arestas_subarvore++;
                }
            }
        }
        return subarvore_precisa_resfriar;
    }
}
