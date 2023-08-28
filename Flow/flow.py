import sys

sys.path.append('../')
from Detection.HardwareCategory import hardware
from Detection.SystemCategory import system
from Detection.CPUCategory import cpu
from UserInterface.interface import *


# initialize checking modules
system = system.SystemChecks()
hardware = hardware.HardwareChecks()
cpu = cpu.CPUChecks()

system_checks = [
    (system.check_system_family, "Checking system family parameter ..."),
    (system.check_files, "Checking for VM related files ..."),
    (system.check_registry_keys, "Checking VM related registry keys ..."),
    # (system.check_software, "Checking for malware analysis related software ..."),
    (system.check_processes, "Checking running processes ..."),
    (system.check_users, "Checking for suspicious users ..."),
    (system.check_uptime, "Checking system uptime ..."),
    (system.check_browser_history, "Checking browser history length ...")
]

hardware_checks = [
    (hardware.check_BIOS, "Checking BIOS ..."),
    (hardware.check_motherboard, "Checking motherboard ..."),
    (hardware.check_hard_drive_size, "Checking hard drive size ..."),
    (hardware.check_hard_drive_model, "Checking hard drive model ..."),
    (hardware.check_RAM_size, "Checking RAM size ..."),
    (hardware.check_MAC_address, "Checking network adapters ..."),
    (hardware.check_CPU_temp, "Checking CPU temperature ..."),
    (hardware.check_CPU_fans, "Checking CPU fans state ...")
]

cpu_checks = [
    (cpu.run_CPUID_id, "Checking CPUID instruction for ID ..."),
    (cpu.run_CPUID_hv, "Checking CPUID instruction for hypervisor bit ..."),
    (cpu.check_CPU_cores, "Checking available CPU cores ...")
]


if __name__ == "__main__":
    print_banner()

    # run system checks
    print_initialize_module("System")
    for check in system_checks:
        run_check(*check)
    print_summary("System", system)

    # run hardware checks
    print_initialize_module("Hardware")
    for check in hardware_checks:
        run_check(*check)
    print_summary("Hardware", hardware)

    # run cpu checks
    print_initialize_module("CPU")
    for check in cpu_checks:
        run_check(*check)
    print_summary("CPU", cpu)

