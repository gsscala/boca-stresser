import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class A {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line != null) {
            StringTokenizer st = new StringTokenizer(line);
            if (st.hasMoreTokens()) {
                int W = Integer.parseInt(st.nextToken());
                int A = Integer.parseInt(st.nextToken());
                int B = Integer.parseInt(st.nextToken());
                int C = Integer.parseInt(st.nextToken());

                if (W >= (A + B + C)) {
                    System.out.println("S");
                } else {
                    System.out.println("N");
                }
            }
        }
    }
}
