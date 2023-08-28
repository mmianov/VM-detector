#include <stdio.h>

int main() {
    int ecx;
    __asm__("mov $0x1 , %eax\n\t");
    __asm__("cpuid\n\t");
    __asm__("mov %%ecx, %0\n\t":"=r" (ecx));
    int hypervisor_present = (ecx >> 31) & 0x1;
    // debug
    // printf("CPUID Hypervisor bit is set to %d",hypervisor_present);
    printf("%d", hypervisor_present);
    return 0;
}
