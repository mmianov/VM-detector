import wmi
import pathlib
import ctypes
import sqlite3
import os
import winreg
import psutil

class SystemChecks:
    def __init__(self):
        self.name = "System Checks"
        self.detection_methods = 8
        self.detection_number = 0
        self.keywords = [
            'VM',
            'VMware',
            'vbox',
            'VritualBox'
        ]

        self.files = [
            "c:\windows\system32\VBoxDispD3D.dll",
            "c:\windows\system32\VBoxHook.dll",
            "c:\windows\system32\VBoxMRXNP.dll",
            "c:\windows\system32\VBoxHook.dll",
            "c:\windows\system32\VBoxSVGA.dll",
            "c:\windows\system32\VBoxGL.dll",
            "c:\windows\system32\VBoxService.exe",
            "c:\windows\system32\VBoxTray.exe",
            "c:\windows\system32\VBoxControl.exe",
            "c:\windows\system32\drivers\VBoxGuest.sys",
            "c:\windows\system32\drivers\VBoxMouse.sys",
            "c:\windows\system32\drivers\VBoxSF.sys",
            "c:\windows\system32\drivers\VBoxWddm.sys",
            "c:\windows\system32\drivers\\vmmouse.sys",
            "c:\windows\system32\drivers\\vmhgfs.sys",
            "c:\windows\system32\drivers\\vmrawdsk.sys",
            "c:\windows\system32\drivers\\vmmemctl.sys",
            "c:\windows\system32\drivers\\vmci.sys",
            "c:\windows\system32\drivers\\vm3dmp.sys",

        ]

        self.software = [
           "idafree",
           "apktool",
           "Bytecode-Viewer",
           "dnSpy",
           "Ghidra",
           "IDR",
           "Capa",
           "Codetrack",
           "Detect-It-Easy",
           "Explorer Suite",
           "GoReSym",
           "innounp",
           "malware-jail",
           "MAP",
           "NETReactorSlayer",
           "PE-bear",
           "peid",
           "PeStudio",
           "ProcessDump",
           "UniExtract2",
           "apimonitor",
           "HollowsHunter",
           "pe-sieve",
           "regshot",
           "scdbg",
           "windbg",
           "OllyDbg",
           "x64dbg",
           "010 Editor",
           "Cmder",
           "Cyberchef",
           "Cygwin",
           "de4dot-cex",
           "Dependency Walker",
           "dll-to-exe",
           "Floss",
           "HashMyFiles",
           "HxD",
           "innoextract",
           "nasm",
           "rundotnetdll",
           "sysinternals",
           "upx",
           "yara",
           "FakeNet-NG",
           "Wireshark",
        ]

        self.filepath = "C:\Program Files"

        self.keys = [
            "HARDWARE\ACPI\DSDT\VBOX__",
            "HARDWARE\ACPI\FADT\VBOX__",
            "HARDWARE\ACPI\RSDT\VBOX__",
            "HARDWARE\ACPI\SSDT\VBOX__",
            "SYSTEM\ControlSet001\Services\VBoxGuest",
            "SYSTEM\ControlSet001\Services\VBoxMouse",
            "SYSTEM\ControlSet001\Services\VBoxSF",
            "SYSTEM\ControlSet001\Services\VBoxService",
            "SYSTEM\ControlSet001\Services\VBoxWddm",
            "SOFTWARE\Oracle\VirtualBox Guest Additions",
            "SOFTWARE\VMware, Inc.\VMware Drivers",
            "SOFTWARE\VMware, Inc.\VMware Tools",
            "SOFTWARE\VMware, Inc.\VMware VGAuth",
            "SOFTWARE\VMware, Inc.\VMwareHostOpen",
            "SYSTEM\ControlSet001\Services\\vmbus",
            "SYSTEM\ControlSet001\Services\\vmci",
            "SYSTEM\ControlSet001\Services\\vmhgfs",
            "SYSTEM\ControlSet001\Services\\vmmouse",
            "SYSTEM\ControlSet001\Services\\vmrawdisk",
            "SYSTEM\ControlSet001\Services\VMTools"
        ]

        self.processes = [
            "VBoxService.exe",
            "VBoxTray.exe",
            "vmtoolsd.exe",
            "vmwaretray.exe",
            "vmacthlp.exe",
            "vmwareuser.exe",
            "vmware.exe",
            "vmount2.exe"
        ]

        self.usernames = [
            "malware",
            "virus",
            "vm",
            "debug",
            "sample",
            "infected",
            "test",
            "sandbox",
            "reverse",
            "analysis",
            "research",
            "payload",
            "vbox",
            "vmware",
        ]

    def check_files(self):
        info = []
        for file in self.files:
            if os.path.isfile(file):
                info.append("Found: " + file)
        if len(info):
            self.detection_number += 1
            return {"detected": 1, "info": info}
        info.append("File check found no irregularities")
        return {"detected": 0, "info": info}

    def check_software(self):
        info = []
        for soft in self.software:
            files = sorted(pathlib.Path(self.filepath).glob('**/*' + soft + '*'))
            if len(files):
                info.append("Found: " + soft)
        if len(info):
            self.detection_number += 1
            return {"detected": 1, "info": info}
        return {"detected": 0, "info": ["Software check found no irregularities"]}

    def check_processes(self):
        info = []
        for proc in psutil.process_iter():
            try:
                process_name = proc.name()
                if process_name in self.processes:
                    info.append("Found: " + process_name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        if len(info) > 0:
            return {"detected": 1, "info": info}
        else:
            return {"detected": 0, "info": "No VM processes found"}

    def check_registry_keys(self):
        info = []
        for key in self.keys:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key):
                    info.append("Found: " + key)
            except FileNotFoundError:
                pass
        if len(info) > 0:
            return {"detected": 1, "info": info}
        else:
            return {"detected": 0, "info": "No VM registry found"}

    def check_users(self):

        wmi_service = wmi.WMI()
        users = wmi_service.Win32_UserAccount()
        info = []
        for user in users:
            if user.name in self.usernames:
                info.append("Suspicious username detected:" + user.Name)
        if len(info):
            self.detection_number += 1
            return {"detected": 1, "info": info}
        else:
            return {"detected": 0, "info": ["No VM usernames detected"]}

    def check_prompt(self):
        """
        Checks for PROMPT environment variable
        :return: value of PROMPT, if it exists
        """
        wmi_service = wmi.WMI()
        info = []
        try:
            env_var = wmi_service.Win32_Environment(Name="PROMPT")[0].VariableValue
            if any(keyword in env_var for keyword in ['VM', 'FLARE', 'COMMANDO']):
                info.append("Found unusual command prompt: " + env_var)
                self.detection_number += 1
                return {"detected": 1, "info": info}
        except:
            return {"detected": 0, "info": ['"PROMPT" env variable not set']}

    def check_uptime(self):
        low_uptime_minutes = 12
        uptime_ms = ctypes.windll.kernel32.GetTickCount64()
        uptime_s = str(uptime_ms)[:-3]
        info = []
        if int(uptime_s) < low_uptime_minutes * 60:
            info.append("System uptime is less than 12 minutes")
            self.detection_number += 1
            return {"detected": 1, "info": info}
        return {"detected": 0, "info": ["No low uptime detected"]}

    def check_browser_history(self):
        chrome_history = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\history'
        min_history_count = 10
        info = []
        try:
            conn = sqlite3.connect(chrome_history)
            cursor = conn.cursor()
            query = "SELECT urls.url FROM urls"
            cursor.execute(query)
            results = cursor.fetchall()
            if len(results) < min_history_count:
                info.append('Chrome browser history low: ' + str(len(results)) + 'visited websites')
                self.detection_number += 1
                return {"detected": 1, "info": info}
            return {"detected": 0, "info": ["Chrome browser history appears normal"]}
        except:
            info.append("Unable to access browser history - database locked!")
            return {"detected": -1, "info": info}

    def check_system_family(self):
        wmi_service = wmi.WMI()
        info = []
        for item in wmi_service.Win32_ComputerSystem():
            family = item.SystemFamily
            if family == 'Virtual Machine':
                info.append("Found: SystemFamily = \"Virtual Machine\"")
                self.detection_number += 1
                return {"detected": 1, "info": info}
            else:
                return {"detected": 0, "info": [f'SystemFamily parameters appears normal: {item.SystemFamily}']}
