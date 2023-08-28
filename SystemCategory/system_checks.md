## System Checks

### 1. VM related files and directories

There are particular files and directories that are specific for virtual environments, for example:
* `c:\windows\system32\drivers\VBoxGuest.sys`
* `c:\windows\system32\drivers\vmnet.sys`
* `c:\windows\system32\vboxtray.exe`
* `C:\Program Files\VMware\VMware Tools\vmtoolsd.exe`
 

### 2. Installed software

Some programs and applications are rarely found on a normal user systems and might indicate 
tools used in a virtual
environment, for example:
* IDA Pro
* Ghidra
* dnSpy 
* perl
* python

### 3. Registry values

Some registry values are virtual environment specific and may idicate running inside VM, for example:
* `HARDWARE\ACPI\DSDT\VBOX__ (VBOX)`
* `SOFTWARE\Oracle\VirtualBox Guest Additions `
* `SYSTEM\ControlSet001\Services\VBoxService (VBOX)`

### 3. Running processes

Malware can check for known virtual environment processes running on the system, for example:
* `VBoxService.exe`
* `VBoxTray.exe`

### 4. Username and hostname

Sometimes virtual machines are configured for the purposes of analysis and reverse engineering,
with username or host name containing specific keywords like:
* malawre
* maltest
* sandbox
* virus


### 4. Environment variables

Some virtual machines distributions might have unique environment variables set, such as `PROMPT`
which is used in two very popular VMs - `Flare VM` and `Commando VM`.


### 5. System uptime

If the system uptime is small, then it might indicate a virtual machine that was just deployed
for the purpose of malware analysis.

### 6. Browser history

Typical user frequently uses some form of Internet browser to carry out everyday tasks which
leaves trails in the form of browser history. Virtual machine deployed for the purpose of malware
analysis might not have any browser history at all.

### 7. Recently opened files
Typical user frequently opens or modifies files on the system which as opposed to a malware analyst
who may never need to create or open files on a virtual system.


