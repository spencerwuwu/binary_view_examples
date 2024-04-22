#include <stdio.h>

// Function declarations
unsigned long long fibonacciIterative(int n);
unsigned long long fibonacciRecursive(int n);

int main() {
    int num;

    // Take input from the user
    printf("Enter the number of terms for Fibonacci sequence: ");
    scanf("%d", &num);

    printf("Fibonacci sequence using iterative method:\n");
    for (int i = 0; i < num; i++) {
        printf("%llu ", fibonacciIterative(i));
    }

    printf("\n\nFibonacci sequence using recursive method:\n");
    for (int i = 0; i < num; i++) {
        printf("%llu ", fibonacciRecursive(i));
    }

    return 0;
}

// Function definition for Fibonacci sequence using iterative method
unsigned long long fibonacciIterative(int n) {
    unsigned long long a = 0, b = 1, temp;

    if (n == 0) {
        return a;
    }
    else if (n == 1) {
        return b;
    }

    for (int i = 2; i <= n; i++) {
        temp = a + b;
        a = b;
        b = temp;
    }

    return b;
}

// Function definition for Fibonacci sequence using recursive method
unsigned long long fibonacciRecursive(int n) {
    if (n <= 1) {
        return n;
    }
    else {
        return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
    }
}
