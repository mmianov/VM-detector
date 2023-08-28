#include <stdio.h>

int main() {
    int reg[4];
    __asm__("mov $0x40000000 , %eax\n\t");
    __asm__("cpuid\n\t");
    __asm__("mov %%ebx, %0\n\t":"=r" (reg[0]));
    __asm__("mov %%ecx, %0\n\t":"=r" (reg[1]));
    __asm__("mov %%edx, %0\n\t":"=r" (reg[2]));
    reg[3] = '\0';
    printf ("%s\n", &reg);
    return 0;
}