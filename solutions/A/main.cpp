#include <iostream>

using namespace std;

int main() {
    // Otimização de I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int W, A, B, C;
    // Lê os 4 inteiros da entrada
    if (cin >> W >> A >> B >> C) {
        // Verifica se a ração restante é suficiente
        if (W >= (A + B + C)) {
            cout << "S\n";
        } else {
            cout << "N\n";
        }
    }
    
    return 0;
}
