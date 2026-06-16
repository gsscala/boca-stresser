#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {
    // Otimização de I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    // Lista completa dos 27 códigos ISO 3166-2 do Brasil
    vector<string> estados = {
        "BR-AC", "BR-AL", "BR-AP", "BR-AM", "BR-BA", "BR-CE", "BR-DF", "BR-ES",
        "BR-GO", "BR-MA", "BR-MT", "BR-MS", "BR-MG", "BR-PA", "BR-PB", "BR-PR",
        "BR-PE", "BR-PI", "BR-RJ", "BR-RN", "BR-RS", "BR-RO", "BR-RR", "BR-SC",
        "BR-SP", "BR-SE", "BR-TO"
    };

    string s;
    if (cin >> s) {
        int correspondencias = 0;
        bool bate_com_sp = false;

        // Testa a string de entrada contra todos os 27 estados
        for (const string& estado : estados) {
            bool eh_compativel = true;
            
            // Compara caractere por caractere
            for (int i = 0; i < 5; i++) {
                // Se o caractere não for o curinga '?' e também não for 
                // igual ao caractere do estado atual, não é compatível
                if (s[i] != '?' && s[i] != estado[i]) {
                    eh_compativel = false;
                    break;
                }
            }
            
            if (eh_compativel) {
                correspondencias++;
                if (estado == "BR-SP") {
                    bate_com_sp = true;
                }
            }
        }

        // Lógica de decisão final baseada nas correspondências
        if (bate_com_sp) {
            if (correspondencias == 1) {
                cout << "S\n"; // Só bateu com SP
            } else {
                cout << "T\n"; // Bateu com SP e com outros (Talvez)
            }
        } else {
            cout << "N\n"; // Não bateu com SP
        }
    }

    return 0;
}
