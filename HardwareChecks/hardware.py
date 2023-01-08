import subprocess
import re
import wmi



def check_BIOS():
    """
    Checks BIOS parameters that can differentiate VM from physical machine
    :return: dictionary with parameters and their values
    """
    print("[*] Checking BIOS info ...")
    wmi_service = wmi.WMI()
    bios_info = wmi_service.Win32_BIOS()[0]
    check_parameters = {
        "BiosVersion": bios_info.BIOSVersion,
        "Caption": bios_info.Caption,
        "Description": bios_info.Description,
        "SoftwareElementID": bios_info.SoftwareElementID,
        "Version": bios_info.Version
    }
    return check_parameters


def check_motherboard():
    """
    Checks motherboard parameters that can differentiate VM from physical machine
    :return: dictionary with parameters and their values
    """
    print("[*] Checking motherboard info ...")
    wmi_service = wmi.WMI()
    motherboard_info = wmi_service.Win32_BaseBoard()[0]
    check_parameters = {
        "Manufacturer": motherboard_info.Manufacturer,
        "Product": motherboard_info.Product,
        "SerialNumber": motherboard_info.SerialNumber
    }
    return check_parameters


def check_MAC_address():
    wmi_service = wmi.WMI()
    network_adapters = wmi_service.Win32_NetworkAdapter()
    vbox_adapters = ['08:00:27']
    vmware_adapters = ['00:05:69', '00:0C:29', '00:1C:14', '00:50:56']

    for adapter in network_adapters:
        if str(adapter.MACAddress)[:8] in vbox_adapters:
            print("[*] Detected VirtualBox adapter: " + adapter.MACAddress)
        elif str(adapter.MACAddress)[:8] in vmware_adapters:
            print("[*] Detected VMware adapter: " + adapter.MACAddress)

    return network_adapters


def check_CPU_temp():
    wmi_service = wmi.WMI()
    processors = wmi_service.Win32_Processor()
    for processor in processors:
        print(processor)


def check_CPU_fans():
    wmi_service = wmi.WMI()
    fans = wmi_service.Win32_Fan()
    if len(fans) <= 0:
        print('No CPU fans class detected')
    else:
        print("CPU fans class detected")

    return len(fans)


def check_hard_drive_size():
    wmi_service = wmi.WMI()
    logical_disks = wmi_service.Win32_LogicalDisk()
    for disk in logical_disks:
        print(disk)
        print("{}: Drive size = {} bytes, Drive free Space = {} bytes".format(disk.DeviceID, disk.Size, disk.FreeSpace))

    return logical_disks


def check_hard_drive_model():
    wmi_service = wmi.WMI()
    hard_drives = wmi_service.Win32_DiskDrive()
    vm_drives = ['VBOX', 'VMware']
    for drive in hard_drives:
      print(drive)
      if any(vm_drive in drive.Model.split(" ") for vm_drive in vm_drives):
        print("[*] VM hard drive detected: " + drive.Model)

    return hard_drives
