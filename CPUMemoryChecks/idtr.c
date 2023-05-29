#include <stdio.h>

long get_idt_base() {
    char idtr[6];
    #if defined (ENV32BIT)
        _asm sidt idtr
    #endif
        return *((unsigned long *)&idtr[2]);
    }

int main() {
    int idt_vm_detect = ((get_idt_base() >> 24) == 0xff);
    printf("%d", idt_vm_detect);
    return 0;
}