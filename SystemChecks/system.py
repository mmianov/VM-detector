import subprocess
import re
import wmi
import pprint


def load_file(file):
    """
    Loads contents of file into a list.
    :param file: file to read from
    :return: content of file in list
    """
    out = []
    f = open(file, 'r')
    for line in f.readlines():
        out.append(str(line).strip('\n'))
    return out


def check_processes(keywords):
    """
    Checks if running processes contain any of provided keywords.
    :param keywords: words to identify processes with
    """
    print("[*] Checking processes ...")
    vm_processes = []
    query = subprocess.run(['wmic', 'process', 'list'], stdout=subprocess.PIPE)
    processes = str(query.stdout).split('C:')

    pattern = "|".join(keywords)
    regex = re.compile(pattern, re.IGNORECASE)

    for process in processes:
        match = regex.search(process)
        if match:
            vm_processes.append(process[match.start():].split(" ", 1)[0])
            print(process[match.start():].split(" ", 1)[0])
    if len(vm_processes):
        return vm_processes
    return '[*] No VM processes found'


def check_prompt():
    """
    Checks for PROMPT environment variable
    :return: value of PROMPT, if it exists
    """
    print('[*] Checking "PROMPT" env variable ...')
    wmi_service = wmi.WMI()
    env_var = wmi_service.Win32_Environment(Name="PROMPT")
    if env_var:
        return env_var
    return '[*] "PROMPT" env variable not set'


def check_users():
    wmi_service = wmi.WMI()
    users = wmi_service.Win32_UserAccount()
    usernames = ['malawre', 'maltest', 'sandbox', 'virus', 'vmware', 'vbox', 'virusclone']
    for user in users:
        if user in usernames:
            print("Suspicious username detected: " + user.Name)
    return users


if __name__ == "__main__":
    # VM_KEYWORDS = load_file('VM_KEYWORDS')
    # check_processes(VM_KEYWORDS)
    # check_users()
    print(check_prompt())


