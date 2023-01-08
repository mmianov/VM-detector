## Hardware Checks

### 1. Motherboard version

Motherboard version can reflect on a virtual machine vendor, as it frequently contains
VM specific keywords such as `VBOX`, `VMWARE`, `ORACLE`.


### 2. BIOS version

BIOS version can reflect on a virtual machine vendor, as it frequently contains
VM specific keywords or VM software vendor.

### 3. Hard drive size and model

Hard disk model can reflect on a virtual machine vendor. While hard disk size cannot 
unequivocally determine virtual machine, it can be a good indicator, since virtual machines
are often given small disk sizes.

### 4. RAM size

Virtual machines are often given RAM sizes that are very rarely used by normal users,
such as 1 GB or 2 GB.

### 5. CPU temperature 

A physical Windows machine can be queried for a CPU temperature which should return a float
or integer value. A virtual machine will likely throw an `ERROR`.

### 6. CPU fans state 

A physical Windows machine can be queried for a CPU fans state which will return a class
with CPU fans statistics. A virtual machine will likely return an empty response.

### 7. MAC addresses and adapter name

Virtual machine vendor have specific MAC address that are given by default to their network
interfaces, for example:
* MAC address starting with `08:00:27` indicates VirtualBox 
* MAC address starting with `00:05:69`, `00:0C:29`, `00:0C:29` or `00:50:56`  indicates VMware 

Additionally, querying for network adapter name or ID can return VM vendor specific keywords.
