import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class B {
    static class Edge {
        int to;
        long weight;
        Edge(int to, long weight) {
            this.to = to;
            this.weight = weight;
        }
    }

    static class Node implements Comparable<Node> {
        int u;
        long dist;
        Node(int u, long dist) {
            this.u = u;
            this.dist = dist;
        }
        @Override
        public int compareTo(Node other) {
            return Long.compare(this.dist, other.dist);
        }
    }

    static final long INF = (long) 2e18;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        StringTokenizer st = new StringTokenizer(line);
        if (!st.hasMoreTokens()) return;
        int N = Integer.parseInt(st.nextToken());
        int M = Integer.parseInt(st.nextToken());
        int K = Integer.parseInt(st.nextToken());

        List<Edge>[] adj = new ArrayList[N + 1];
        for (int i = 1; i <= N; i++) adj[i] = new ArrayList<>();

        for (int i = 0; i < M; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            long c = Long.parseLong(st.nextToken());
            adj[u].add(new Edge(v, c));
            adj[v].add(new Edge(u, c));
        }

        st = new StringTokenizer(br.readLine());
        int[] entradas = new int[K];
        for (int i = 0; i < K; i++) {
            entradas[i] = Integer.parseInt(st.nextToken());
        }

        long[] tempo_pessoas = new long[N + 1];
        Arrays.fill(tempo_pessoas, INF);
        PriorityQueue<Node> pq = new PriorityQueue<>();

        for (int e : entradas) {
            tempo_pessoas[e] = 0;
            pq.add(new Node(e, 0));
        }

        while (!pq.isEmpty()) {
            Node current = pq.poll();
            int u = current.u;
            long d = current.dist;

            if (d > tempo_pessoas[u]) continue;

            for (Edge edge : adj[u]) {
                long tempo_aresta = 2 * edge.weight;
                if (tempo_pessoas[u] + tempo_aresta < tempo_pessoas[edge.to]) {
                    tempo_pessoas[edge.to] = tempo_pessoas[u] + tempo_aresta;
                    pq.add(new Node(edge.to, tempo_pessoas[edge.to]));
                }
            }
        }

        long left = 0, right = (long) 2e14;
        long ans = right;

        while (left <= right) {
            long mid = left + (right - left) / 2;
            if (testaCaminho(mid, N, adj, tempo_pessoas)) {
                ans = mid;
                right = mid - 1;
            } else {
                left = mid + 1;
            }
        }
        System.out.println(ans);
    }

    static boolean testaCaminho(long X, int N, List<Edge>[] adj, long[] tempo_pessoas) {
        long[] tempo_carlos = new long[N + 1];
        Arrays.fill(tempo_carlos, INF);
        PriorityQueue<Node> pq = new PriorityQueue<>();

        if (-X <= tempo_pessoas[1]) {
            tempo_carlos[1] = -X;
            pq.add(new Node(1, -X));
        }

        while (!pq.isEmpty()) {
            Node current = pq.poll();
            int u = current.u;
            long d = current.dist;

            if (d > tempo_carlos[u]) continue;
            if (u == N) return true;

            for (Edge edge : adj[u]) {
                long tempo_chegada = tempo_carlos[u] + edge.weight;
                if (tempo_chegada <= tempo_pessoas[edge.to] && tempo_chegada < tempo_carlos[edge.to]) {
                    tempo_carlos[edge.to] = tempo_chegada;
                    pq.add(new Node(edge.to, tempo_carlos[edge.to]));
                }
            }
        }
        return false;
    }
}
