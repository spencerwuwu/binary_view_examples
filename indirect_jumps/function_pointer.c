#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>


void func1(int a) {
    printf("func1: %d\n", a);
}

void func2(int a) {
    printf("func2: %d\n", a);
}

typedef struct {
    void (*func)(int);
    int arg;
} FuncState;


void (*Functions[2])(int) = {
    func1,
    func2
};

int main() {
    int input;
    scanf("%d", &input);

    FuncState *state = malloc(sizeof(FuncState));

    if (input == 0) {
        state->func = func1;
        state->arg = 0;
    } else {
        state->func = Functions[input%2];
        state->arg = input;
    }
    (state->func)(state->arg);

    return 0;
}
