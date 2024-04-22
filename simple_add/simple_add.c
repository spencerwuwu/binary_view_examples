#include <stdio.h>

// Function declarations
void greet();
int add(int a, int b);

int main() {
    // Function calls
    greet();
    
    int num1 = 10;
    int num2 = 20;
    int sum = add(num1, num2);
    
    printf("The sum of %d and %d is %d\n", num1, num2, sum);
    
    return 0;
}

// Function definitions
void greet() {
    printf("Hello!\n");
}

int add(int a, int b) {
    return a + b;
}

