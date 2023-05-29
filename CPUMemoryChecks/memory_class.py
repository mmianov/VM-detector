import subprocess


class CPUMemoryChecks:
    def __init__(self):
        self.name = "CPU and Memory Checks"
        self.detection_methods = 2
        self.detection_number = 0
        self.id_keyword = ['Vbox', 'VMware']

    def run_CPUID(self):
        try:
            completed_process = subprocess.run("CPUMemoryChecks/cpuid.exe", stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            stdout_output = str(completed_process.stdout)
            id = ""
            for c in stdout_output:
                if c == "\\":
                    break
                id += c
            if id in self.id_keyword:
                self.detection_number += 1
                return {"detected": 1, "info":["CPUID instruction returned: " + id]}
            return {"detected": 0, "info":["CPUID returned regular CPU identifier"]}
        except:
            return {"detected": -1, "info": ["Cannot run CPUID detection method!"]}

    def check_IDGT(self):
        try:
            completed_process = subprocess.run("CPUMemoryChecks/idtr.exe", stdout=subprocess.PIPE,
                                               stderr=subprocess.DEVNULL)
            stdout_output = int(completed_process.stdout)
            if stdout_output == 0:
                return {"detected": 0, "info": ["IDTR relocation has not been detected"]}
            self.detection_number +=1
            return {"detected": 1, "info": ["IDTR relocated!"]}
        except:
            return {"detected": -1, "info": ["Cannot run IDTR detection method!"]}



