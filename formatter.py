from rich.console import Console
from rich.status import Status
from rich.theme import Theme
from rich.padding import Padding
import time
from datetime import datetime


output_theme = Theme({
    "date": "white",
    "info": "bold white",
    "passed": "bold green",
    "warning": "bold dark_orange",
    "warning_info": "dark_orange",
    "detected": "bold red1",
    "detected_info": "red3"
})
console = Console(theme=output_theme)


def print_banner():
    banner = '''
██╗   ██╗███╗   ███╗      ██████╗ ███████╗████████╗███████╗ ██████╗████████╗ ██████╗ ██████╗ 
██║   ██║████╗ ████║      ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║   ██║██╔████╔██║█████╗██║  ██║█████╗     ██║   █████╗  ██║        ██║   ██║   ██║██████╔╝
╚██╗ ██╔╝██║╚██╔╝██║╚════╝██║  ██║██╔══╝     ██║   ██╔══╝  ██║        ██║   ██║   ██║██╔══██╗
 ╚████╔╝ ██║ ╚═╝ ██║      ██████╔╝███████╗   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
  ╚═══╝  ╚═╝     ╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

    '''
    console.print(f"{banner}")

    console.print(f"[medium_purple3]Author: Mateusz Mianowany")
    console.print(f"[medium_purple3]Version: 1.1")
    time, date = datetime.now().strftime("%H:%M"), datetime.now().strftime("%d-%m-%Y")
    console.print(f"[medium_purple3]Up and running: {date} {time}\n")


def run_check(check, info):
    status = Status(f"[info]" + info + "[/info]", console=console, spinner_style="bold medium_purple3")
    status.start()
    result = check()
    status.stop()
    if result['detected'] == 0:
        console.print(f"[[passed]*[/passed]] [info]{info} [/info] [passed] OK [/passed]")
    elif result["detected"] == -1:
        console.print(f"[[warning]*[/warning]] [info]{info} [/info] [warning] ERROR [/warning]")
        for detection_info in result["info"]:
            console.print(Padding(f"[warning_info]{detection_info}[/warning_info]", (0, 0, 0, 4)))
    else:
        console.print(f"[[detected]*[/detected]] [info]{info} [/info] [detected] DETECTED [/detected]")
        for detection_info in result["info"]:
            time.sleep(0.4)
            console.print(Padding(f"[detected_info]{detection_info}[/detected_info]", (0, 0, 0, 4)))


def print_initialize_module(check_type):
    return console.print(f"[bold medium_purple3][!] {check_type} module initialized ")


def print_summary(check_type, check_object):
    return console.print(f"[bold medium_purple3][!] {check_type} Checks finished: " + str(check_object.detection_number)
                         + "/" + str(check_object.detection_methods) + " methods detected VM or VM-related artifacts on the system.")
