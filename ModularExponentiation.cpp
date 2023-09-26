#include<bits/stdc++.h>
#include<cmath>

using namespace std;

long long power(long long n, long long p) {
    long long result = 1;

    for (int i=0; i<p; ++i) {
        result *= n;
    }

    return result;
}

vector<int> intToBinary(int n) {
    int leftoverN = n;

    vector<int> powersOf2 = {};

    while (leftoverN != 0) {
        int currentExponent = 0;
        int valueToSubtract = power(2, currentExponent);

        while (valueToSubtract < leftoverN) {
            if (currentExponent == 0) {
                currentExponent += 2;
            }
            else {
                currentExponent *= 2;
            }
            valueToSubtract = power(2, currentExponent);
        }

        for (valueToSubtract; valueToSubtract>0; valueToSubtract/=2) {
            if (valueToSubtract <= leftoverN) {
                leftoverN -= valueToSubtract;
                powersOf2.push_back(valueToSubtract);
                break;
            }
        }
    }

    return powersOf2;
}

int miniExponentMod(int a, int b, int c) {
    long long r = a % c;
    for (int i=2; i<=b; i*=2) {
        r = power(r, 2);
        r %= c;
    }

    return r;
}


long long findExponentMod(int a, int b, int c) { // A^B mod C = return value.
    // turn b into binary value
    // get powers of 2 that make up b
    // for all powers of 2, mod c for a to the power of each value.
    vector<int> powersOf2 = intToBinary(b);
    __int128 val = miniExponentMod(a, powersOf2[0], c);

    for (int i=1; i<powersOf2.size(); i++) {
        val *= miniExponentMod(a, powersOf2[i], c);
    }
    return val % c;
}


int main() {
    while (true) {
        int a, b, c;
        cout << "Input Format:" << "\n";
        cout << "a -> b -> c" << "\n";
        cout << "where (a^b) mod c" << "\n";
        cin >> a >> b >> c;
        cout << "Ans: " << findExponentMod(a, b, c) << "\n";
    }

    ios::sync_with_stdio(0);
    cin.tie(0);
    return 0;
}

// ABOUT THIS PROJECT
// Made this in the midst of learning modular arithmetic, and decided to write a program for fast modular exponentiation. This is by no means the 
// fastest method but my own code implementation of fast modular exponentiation. It involves splitting the exponents into multiples powers of 2, 
// which is done by converting it to a base 2 format, and then using the modular multiplication properties to get the final value. I struggled a 
// little while writing this due to unfamiliarity with C++ and its integer limitations. I kept getting invalid values that were clearly overflow, 
// and had to manually work the numbers out in order to find a fitting integer type, and settled on a 128-bit integer. I feel this is a problem any 
// programmer pampered by dynamic typing would face.
