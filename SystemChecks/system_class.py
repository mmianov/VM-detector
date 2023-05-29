import subprocess
import re
import wmi
from datetime import datetime
import pathlib
import ctypes
import sqlite3
import os


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
            'c:\windows\system32\drivers\VBoxMouse.sys',  # VBox
            'c:\windows\system32\drivers\VBoxGuest.sys',
            'c:\windows\system32\drivers\VBoxSF.sys',
            'c:\windows\system32\drivers\VBoxVideo.sys',
            'c:\windows\system32\vboxdisp.dll',
            'c:\windows\system32\vboxhook.dll',
            'c:\windows\system32\vboxmrxnp.dll',
            'c:\windows\system32\vboxogl.dll',
            'c:\windows\system32\vboxoglarrayspu.dll',
            'c:\windows\system32\vboxoglcrutil.dll',
            'c:\windows\system32\vboxoglerrorspu.dll',
            'c:\windows\system32\vboxoglfeedbackspu.dll',
            'c:\windows\system32\vboxoglpackspu.dll',
            'c:\windows\system32\vboxoglpassthroughspu.dll',
            'c:\windows\system32\vboxservice.exe',
            'c:\windows\system32\vboxtray.exe',
            'c:\windows\system32\VBoxControl.exe',
            'c:\windows\system32\drivers\vmmouse.sys',  # VMware
            'c:\windows\system32\drivers\vmnet.sys',
            'c:\windows\system32\drivers\vmxnet.sys',
            'c:\windows\system32\drivers\vmhgfs.sys',
            'c:\windows\system32\drivers\vmx86.sys',
            'c:\windows\system32\drivers\hgfs.sys'
        ]
        self.software = [
            'wireshark',
            'IDA Pro',
            'ghidra',
            'ollydbg',
            'windbg',
            'sysmon',
            'radare2',
            'pdfid',
            'yara',
            'Binary Ninja',
            'dnSpy',
            'RegShot',
        ]
        self.usernames = ['malawre', 'maltest', 'sandbox', 'virus', 'vmware', 'vbox', 'virusclone']

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
            files = sorted(pathlib.Path('C:\Program Files').glob('**/*' + soft + '*'))
            if len(files):
                info.append("Found: " + soft)
        if len(info):
            self.detection_number += 1
            return {"detected": 1, "info": info}
        return {"detected": 0, "info": ["Software check found no irregularities"]}

    def check_processes(self):
        """
        Checks if running processes contain any of provided keywords.
        :param keywords: words to identify processes with
        """
        vm_processes = []
        info = []
        query = subprocess.run(['wmic', 'process', 'list'], stdout=subprocess.PIPE)
        processes = str(query.stdout).split('C:')

        pattern = "|".join(self.keywords)
        regex = re.compile(pattern, re.IGNORECASE)

        for process in processes:
            match = regex.search(process)
            if match:
                proc = process[match.start():].split(" ", 1)[0]
                if 'VM-detector' not in proc:
                    vm_processes.append(proc)
        if len(vm_processes):
            for proc in set(vm_processes):
                if proc[-1] == "\"":
                    proc = proc[:-1]
                info.append("Found: " + proc)
            self.detection_number += 1
            return {"detected": 1, "info": info}
        return {"detected": 0, "info": ["No VM processes found"]}

    def check_users(self):

        wmi_service = wmi.WMI()
        users = wmi_service.Win32_UserAccount()
        info = []
        for user in users:
            if user in self.usernames:
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
        min_history_count = 5
        info = []
        try:
            conn = sqlite3.connect(chrome_history)
            cursor = conn.cursor()
            query = "SELECT urls.url, visits.visit_time FROM urls INNER JOIN visits ON urls.id = visits.url;"
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
