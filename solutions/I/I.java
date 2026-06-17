import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.*;

public class I {
    static final long MOD = 998244353;

    static class State {
        int len, link;
        int[] next = new int[2];
        State() {
            Arrays.fill(next, -1);
        }
    }

    static State[] st;
    static int sz, last;

    static void sam_init(int maxlen) {
        st = new State[maxlen * 2];
        for (int i = 0; i < maxlen * 2; i++) st[i] = new State();
        st[0].len = 0;
        st[0].link = -1;
        sz = 1;
        last = 0;
    }

    static void sam_extend(int c) {
        int cur = sz++;
        st[cur].len = st[last].len + 1;
        int p = last;
        while (p != -1 && st[p].next[c] == -1) {
            st[p].next[c] = cur;
            p = st[p].link;
        }
        if (p == -1) {
            st[cur].link = 0;
        } else {
            int q = st[p].next[c];
            if (st[p].len + 1 == st[q].len) {
                st[cur].link = q;
            } else {
                int clone = sz++;
                st[clone].len = st[p].len + 1;
                st[clone].next = st[q].next.clone();
                st[clone].link = st[q].link;
                while (p != -1 && st[p].next[c] == q) {
                    st[p].next[c] = clone;
                    p = st[p].link;
                }
                st[q].link = st[cur].link = clone;
            }
        }
        last = cur;
    }

    static class Transition {
        long k;
        boolean is_full;
        int end_node;
        long end_len;
        long matches;
    }

    static Transition combine(Transition A, Transition B) {
        Transition C = new Transition();
        C.is_full = A.is_full && B.is_full;
        C.k = (A.is_full ? A.k + B.k : A.k) % MOD;
        C.end_node = B.end_node;
        if (C.is_full) {
            C.end_len = C.k;
        } else {
            C.end_len = B.is_full ? (A.end_len + B.k) % MOD : B.end_len;
        }
        long extra = B.matches;
        if (A.is_full) {
            extra = (extra + B.k * A.k) % MOD;
        } else {
            extra = (extra + B.k * A.end_len) % MOD;
        }
        C.matches = (A.matches + extra) % MOD;
        return C;
    }

    static Transition make_char_transition(int node, char ch) {
        int c = (ch == 'S') ? 0 : 1;
        Transition T = new Transition();
        if (st[node].next[c] != -1) {
            T.is_full = true;
            T.k = 1;
            T.end_node = st[node].next[c];
            T.end_len = 1;
            T.matches = 1;
        } else {
            T.is_full = false;
            T.k = 0;
            int curr = st[node].link;
            int len = 0;
            while (curr != -1 && st[curr].next[c] == -1) {
                curr = st[curr].link;
            }
            if (curr != -1) {
                len = st[curr].len;
                curr = st[curr].next[c];
                len++;
            } else {
                curr = 0;
                len = 0;
            }
            T.end_node = curr;
            T.end_len = len;
            T.matches = len;
        }
        return T;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String A = br.readLine();
        if (A == null) return;
        int N = Integer.parseInt(br.readLine().trim());
        StringTokenizer stTok = new StringTokenizer(br.readLine());
        int[] T_arr = new int[N];
        int max_T = 0;
        for (int i = 0; i < N; i++) {
            T_arr[i] = Integer.parseInt(stTok.nextToken());
            if (T_arr[i] > max_T) max_T = T_arr[i];
        }

        sam_init(A.length());
        for (char c : A.toCharArray()) sam_extend(c == 'S' ? 0 : 1);

        Transition[] trans_S = new Transition[sz];
        Transition[] trans_P = new Transition[sz];
        for (int i = 0; i < sz; i++) {
            trans_S[i] = make_char_transition(i, 'S');
            trans_P[i] = make_char_transition(i, 'P');
        }

        Transition[][] trans_memo = new Transition[max_T + 1][sz];
        if (max_T >= 1) {
            for (int i = 0; i < sz; i++) {
                trans_memo[1][i] = combine(trans_S[i], trans_P[trans_S[i].end_node]);
            }
        }

        for (int t = 2; t <= max_T; t++) {
            for (int i = 0; i < sz; i++) {
                Transition t1 = trans_S[i];
                Transition t2 = trans_memo[t - 1][t1.end_node];
                Transition t3 = combine(t1, t2);
                Transition t4 = trans_memo[t - 1][t3.end_node];
                trans_memo[t][i] = combine(t3, t4);
            }
        }

        long total_intervals = 0;
        int curr_node = 0;
        long curr_len = 0;
        for (int i = 0; i < N; i++) {
            int t = T_arr[i];
            Transition tr = trans_memo[t][curr_node];
            long added = (tr.k * curr_len + tr.matches) % MOD;
            total_intervals = (total_intervals + added) % MOD;
            if (tr.is_full) {
                curr_len = (curr_len + tr.k) % MOD;
            } else {
                curr_len = tr.end_len;
            }
            curr_node = tr.end_node;
        }
        System.out.println(total_intervals);
    }
}
