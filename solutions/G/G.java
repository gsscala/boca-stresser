import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class G {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null) return;
        s = s.trim();
        if (s.isEmpty()) return;

        String[] estados = {
            "BR-AC", "BR-AL", "BR-AP", "BR-AM", "BR-BA", "BR-CE", "BR-DF", "BR-ES",
            "BR-GO", "BR-MA", "BR-MT", "BR-MS", "BR-MG", "BR-PA", "BR-PB", "BR-PR",
            "BR-PE", "BR-PI", "BR-RJ", "BR-RN", "BR-RS", "BR-RO", "BR-RR", "BR-SC",
            "BR-SP", "BR-SE", "BR-TO"
        };

        int correspondencias = 0;
        boolean bate_com_sp = false;

        for (String estado : estados) {
            boolean eh_compativel = true;
            for (int i = 0; i < 5; i++) {
                if (s.charAt(i) != '?' && s.charAt(i) != estado.charAt(i)) {
                    eh_compativel = false;
                    break;
                }
            }
            if (eh_compativel) {
                correspondencias++;
                if (estado.equals("BR-SP")) {
                    bate_com_sp = true;
                }
            }
        }

        if (bate_com_sp) {
            if (correspondencias == 1) {
                System.out.println("S");
            } else {
                System.out.println("T");
            }
        } else {
            System.out.println("N");
        }
    }
}
