import wmi
from Detection.HardwareCategory.utils import convert_bytes


class HardwareChecks:
    def __init__(self):
        self.name = "Hardware Checks"
        self.detection_methods = 8
        self.detection_number = 0
        self.keywords = [
            'VM',
            'VMware',
            'vmware',
            'vbox',
            'VritualBox',
            'virtualbox',
            'oracle'
        ]
        self.vbox_adapters = ['08:00:27']
        self.vmware_adapters = ['00:05:69', '00:0C:29', '00:1C:14', '00:50:56']
        self.low_hard_drive_size = 64424509440
        self.low_ram_size = 2147483648

    def check_BIOS(self):
        """
        Checks BIOS parameters that can differentiate VM from physical machine
        :return: dictionary with parameters and their values
        """
        wmi_service = wmi.WMI()
        bios_info = wmi_service.Win32_BIOS()[0]
        info = []
        for version in bios_info.BIOSVersion:
            if any(keyword in version.lower() for keyword in self.keywords):
                info.append("Found BIOS Version: " + version)
        if any(keyword in bios_info.Caption.lower() for keyword in self.keywords):
            info.append("Found BIOS Caption: " + bios_info.Caption)
        if any(keyword in bios_info.Description.lower() for keyword in self.keywords):
            info.append("Found BIOS Description: " + bios_info.Description)
        if any(keyword in bios_info.SoftwareElementID.lower() for keyword in self.keywords):
            info.append("Found BIOS SoftwareElementID: " + bios_info.SoftwareElementID)
        detected = len(info)
        if detected:
            self.detection_number += 1
        return {"detected": detected, "info": info}

    def check_motherboard(self):
        """
        Checks motherboard parameters that can differentiate VM from physical machine
        :return: dictionary with parameters and their values
        """
        wmi_service = wmi.WMI()
        motherboard_info = wmi_service.Win32_BaseBoard()[0]
        info = []
        if any(keyword in motherboard_info.Manufacturer.lower() for keyword in self.keywords):
            info.append("Found manufacturer: " + motherboard_info.Manufacturer)
        if any(keyword in motherboard_info.Product.lower() for keyword in self.keywords):
            info.append("Found product value: " + motherboard_info.Product)
        if motherboard_info.SerialNumber in ['0','None'] :
            info.append("Found unusual serial number: " + motherboard_info.SerialNumber)
        detected = len(info)
        if detected:
            self.detection_number += 1
        return {"detected": detected, "info": info}

    def check_hard_drive_size(self):
        wmi_service = wmi.WMI()
        logical_disks = wmi_service.Win32_LogicalDisk()
        low_disks = []
        info = []
        for disk in logical_disks:
            if int(disk.size) < self.low_hard_drive_size:  # -> changed to 60 GB
                low_disks.append([disk.DeviceID, convert_bytes(int(disk.Size)), convert_bytes(int(disk.FreeSpace))])
        if len(low_disks):
            for disk in low_disks:
                info.append("Size of: " + disk[0] + "is lower than 60 GB")
            self.detection_number += 1
        return {"detected": len(low_disks) > 0, "info": info}

    def check_hard_drive_model(self):
        wmi_service = wmi.WMI()
        hard_drives = wmi_service.Win32_DiskDrive()
        vm_drives = ['VBOX', 'VMware']
        info = []
        for drive in hard_drives:
            if any(vm_drive in drive.Model.split(" ") for vm_drive in vm_drives):
                info.append("VM hard drive detected: " + drive.Model)
                self.detection_number += 1
                return {"detected": 1, "info": info}
            elif any(vm_drive in drive.Caption.split(" ") for vm_drive in vm_drives):
                info.append("VM hard drive detected: " + drive.Caption)
                self.detection_number += 1
                return {"detected": 1, "info": info}
            else:
                info.append("Hard drive check returned no irregularities.")
                return {"detected": 0, "info": info}

    def check_RAM_size(self):
        wmi_service = wmi.WMI()
        info = []
        for item in wmi_service.Win32_ComputerSystem():
            total_ram = int(item.TotalPhysicalMemory)
            size = convert_bytes(total_ram)
            if total_ram < self.low_ram_size:
                info.append("Low RAM size detected: " + str(size[0]) + size[1])
                self.detection_number += 1
                return {"detected": 1, "info": info}
            else:
                info.append("Regular RAM size: " + str(size[0]) + size[1])
                return {"detected": 0, "info": convert_bytes(total_ram)}

    def check_MAC_address(self):
        wmi_service = wmi.WMI()
        network_adapters = wmi_service.Win32_NetworkAdapter()
        info = []
        for adapter in network_adapters:
            if str(adapter.MACAddress)[:8] in self.vbox_adapters:
                info.append("Detected VirtualBox adapter: " + adapter.MACAddress)
                self.detection_number += 1
                return {"detected": 1, "info": info}
            elif str(adapter.MACAddress)[:8] in self.vmware_adapters:
                info.append("Detected VMware adapter:  00:50:56:C0:00:01")
                self.detection_number += 1
                return {"detected": 1, "info": info}
        info.append("MAC address check returned no irregularities")
        return {"detected": 0, "info": info}

    # TODO - zmiana na błąd -> VMka ?
    def check_CPU_temp(self):
        wmi_service = wmi.WMI()
        try:
            temperature = wmi_service.Win32_TemperatureProbe()
            if not temperature:
                return {"detected": -1, "info": ["CPU temperature information is not accessible!"]}
            else:
                if temperature[0].Availability:
                    return {"detected": 0, "info": ["CPU temperature is accessible"]}
                self.detection_number += 1
                return {"detected": 1, "info": ["CPU temperature is NOT available!"]}
        except:
            return {"detected": -1, "info": ["There was an error accessing CPU temperature information!"]}

    def check_CPU_fans(self):
        wmi_service = wmi.WMI()
        try:
            fans = wmi_service.Win32_Fan()
            if not fans:
                self.detection_number += 1
                return {"detected": 1, "info": ["CPU fans NOT available!"]}
            else:
                return {"detected": 0, "info": ["CPU fans information is accessible"]}
        except:
            return {"detected": -1, "info": ["There was an error accessing CPU fans information!"]}

