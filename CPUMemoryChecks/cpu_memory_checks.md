## Program Execution and Memory Checks

### 1. CPUID instruction return value

The CPUID instruction is an instruction that returns processor identification 
to EBX, ECX, EDX registers which can identify a VM vendor.



### 2. CPU register initial values

Some virtual machines initialize their register with specific values that can identify them as VMs.


### 3. Stack address range 

Some operating systems have a typical range of memory address that are allocated to the stack upon
program execution. If the stack address range differs, it might be a signal for malware that it
is being ran in a virtual environment.

### 4. Loaded DLLs
Malware can check if virtual environment specific DLLs are loaded into memory.

### 5. DLL addess space

DLLs are located in predictable, non-ASLR memory regions. By checking the address range of some known
DLLs (such as `kernel32.dll`) malware can potentially identify if it is running inside a virtual machine.

### 6. IDT/GDT/LDT tables location

Malware can look at the pointers to important OS tables that are 
usually relocated on a virtual machine. There is usually only one:
* Interrupt Descriptor Table Register (IDTR)
* Global Descriptor Table Register (GDTR)
* Local Descriptor Table Register (LDTR)

per CPU. For this reason, tables have to be moved to a different location when VM gues system
is running to avoid conflicts with the host system.


