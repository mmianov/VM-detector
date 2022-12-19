# Virtual Machine detection methods

## System Checks
* Checking running processes
* WMI queries:
  * model of hard drive or motherboard 
  * OS version
  * BIOS version
  * MAC addresses specific to VMs
  * CPU temperature
  * state of CPU fans
  * number of CPU cores
  * hard drive memory size
* Registry key value checks for VM values
* Checking files of C:\ and D:\ drives
* Checking console prompt for popular VMs



## Program Execution Checks

* CPU registers initial values
* Stack address range 
* DLL address space 
* Checking for loaded DLLs:
  * SbieDll.dll,
  * Dbghelp.dll,
  * Api_log.dll,
  * Dir_watch.dll.
* CPUID return value


**Please note that the list is actively being updated.**


    