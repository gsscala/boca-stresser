#include <iostream>
#include <vector>

int main() {
    // Try to allocate a huge amount of memory
    std::vector<long long> v;
    try {
        while(true) {
            v.push_back(42);
        }
    } catch (...) {}
    return 0;
}
