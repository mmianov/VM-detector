import subprocess
import wmi

class CPUChecks:
    def __init__(self):
        self.name = "CPU and Memory Checks"
        self.detection_methods = 3
        self.detection_number = 0
        self.id_keyword = ['Vbox', 'VMware']

    def run_CPUID_id(self):
        try:
            completed_process = subprocess.run("../Detection/CPUCategory/CPUID-id/cpuid-id.exe", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            stdout_output = str(completed_process.stdout)
            id = ""
            for c in stdout_output:
                if c == "\\":
                    break
                id += c
            if id in self.id_keyword:
                self.detection_number += 1
                return {"detected": 1, "info": ["CPUID instruction returned: " + id]}
            return {"detected": 0, "info": ["CPUID returned regular CPU identifier"]}
        except:
            return {"detected": -1, "info": ["Cannot run CPUID detection method!"]}

    def run_CPUID_hv(self):
        try:
            completed_process = subprocess.run("../Detection/CPUCategory/CPUID-hypervisor-bit/cpuid-hv.exe", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            stdout_output = str(completed_process.stdout)
            if stdout_output == '1':
                return {"detected": 1, "info": ["CPUID hypervisor bit set to 1"]}
            else:
                return {"detected": 0, "info": ["CPUID hypervisor bit set to 0"]}
        except:
            return {"detected": -1, "info": ["Cannot run CPUID detection method!"]}

    def check_CPU_cores(self):
        w = wmi.WMI()
        try:
            cpu = w.Win32_Processor()[0]
            if cpu.NumberOfCores < 2:
                return {"detected": 1, "info": ["Low number of CPU cores detected: " + str(cpu.NumberOfCores)]}
            else:
                return {"detected": 0, "info": ["Acceptable number of CPU cores: " + str(cpu.NumberOfCores)]}
        except:
            return {"detected": -1, "info": ["Unable to access CPU information!"]}



