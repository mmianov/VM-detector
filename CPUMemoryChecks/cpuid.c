#include <stdio.h>

int main() {
    int a[3];
    __asm__("mov $0x0, %eax\n\t");
    __asm__("cpuid\n\t");
    __asm__("mov %%ebx, %0\n\t":"=r" (a[0]));
    __asm__("mov %%edx, %0\n\t":"=r" (a[1]));
    __asm__("mov %%ecx, %0\n\t":"=r" (a[2]));
    printf ("%s\n", &a);
    return 0;
}

