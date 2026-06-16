#include <iostream>

void recurse(int n) {
    int arr[1024]; // Large frame
    for(int i=0; i<1024; i++) arr[i] = n;
    recurse(n + 1);
}

int main() {
    recurse(0);
    return 0;
}
