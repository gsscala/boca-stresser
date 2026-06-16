#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Estrutura para representar um ponto 2D
struct Point {
    long long x, y;
};

// Vértices do polígono listados na ordem dada no problema
const vector<Point> sao_paulo = {
    {0, 100}, {100, 0}, {200, 0}, {100, -100}, 
    {0, -100}, {-100, 0}, {-200, 0}, {-100, 100}
};

// Calcula o produto vetorial entre os vetores (b-a) e (c-a)
long long crossProduct(Point a, Point b, Point c) {
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

// Verifica se o ponto p está no segmento de reta ab
bool onSegment(Point p, Point a, Point b) {
    // Se o produto vetorial for 0, os pontos são colineares
    if (crossProduct(a, b, p) == 0) {
        // Verifica se p está dentro do retângulo delimitado por a e b
        if (p.x >= min(a.x, b.x) && p.x <= max(a.x, b.x) &&
            p.y >= min(a.y, b.y) && p.y <= max(a.y, b.y)) {
            return true;
        }
    }
    return false;
}

// Implementação do Algoritmo Ray Casting
bool isInsideOrOnBorder(Point p, const vector<Point>& poly) {
    int n = poly.size();
    bool inside = false;

    // Iterar pelas arestas do polígono (de i até j)
    for (int i = 0, j = n - 1; i < n; j = i++) {
        
        // 1. O ponto está na fronteira do polígono?
        if (onSegment(p, poly[i], poly[j])) {
            return true;
        }

        // 2. Lançamento de raio para direita
        // Checa se o raio intercepta o segmento de reta
        if (((poly[i].y > p.y) != (poly[j].y > p.y))) {
            // Calcula a interseção X para saber se cruza à direita do ponto
            double intersectX = (poly[j].x - poly[i].x) * (p.y - poly[i].y) / (double)(poly[j].y - poly[i].y) + poly[i].x;
            
            if (p.x < intersectX) {
                inside = !inside;
            }
        }
    }

    return inside;
}

int main() {
    // Otimização de tempo de I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int N;
    if (cin >> N) {
        for (int i = 0; i < N; i++) {
            Point p;
            cin >> p.x >> p.y;

            if (isInsideOrOnBorder(p, sao_paulo)) {
                cout << "S\n";
            } else {
                cout << "N\n";
            }
        }
    }

    return 0;
}
