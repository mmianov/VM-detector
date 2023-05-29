from HardwareChecks.hardware_class import HardwareChecks
from SystemChecks.system_class import SystemChecks
from CPUMemoryChecks.memory_class import CPUMemoryChecks
from formatter import *


# initialize checking modules
hardware = HardwareChecks()
system = SystemChecks()
cpu = CPUMemoryChecks()


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

system_checks = [
    (system.check_system_family, "Checking system family parameter ..."),
    (system.check_files, "Checking for VM related files ..."),
    (system.check_software, "Checking for malware analysis related software ..."),
    (system.check_processes, "Checking for running processes ..."),
    (system.check_users, "Checking for suspicious users ..."),
    (system.check_prompt, "Checking for environment variables ..."),
    (system.check_uptime, "Checking system uptime ..."),
    (system.check_browser_history, "Checking browser history length ...")
]

cpu_checks = [
    (cpu.run_CPUID, "Checking CPUID instruction ..."),
    (cpu.check_IDGT, "Checking IDGT relocation ...")
]


if __name__ == "__main__":
    print_banner()

    # run hardware checks
    print_initialize_module("Hardware")
    for check in hardware_checks:
        run_check(*check)
    print_summary("Hardware", hardware)

    # run system checks
    print_initialize_module("System")
    for check in system_checks:
        run_check(*check)
    print_summary("System", system)

    # run cpu and memory checks
    print_initialize_module("CPU and Memory")
    for check in cpu_checks:
        run_check(*check)
    print_summary("CPU and Memory", cpu)
