# Analysis of detection methods using hardware checks

## BIOS information 

`check_BIOS()` function queries WMI for information about BIOS. Parameters that can quickly identify a virtual
machine are:
* BiosVersion
* Caption
* Description
* SoftwareElementID
* Version

**Physical machine:**

![check_BIOS() on windows](images/bios_win.png)

**Virtual machine:**

![check_BIOS()on vm](images/bios_vm.png)


## Motherboard information

`check_motherboard()` functions queries WMI for information about computer's motherboard.


**Physical machine:**

![check_motherboard() on windows](images/motherboard_win.png)

**Virtual machine:**

![check_motherboard() on vm](images/motherboard_vm.png)
