# VM-Detector
* Author: Mateusz Mianowany
* Affiliation: Warsaw University of Technology
* Thesis subject: Analysis of virtual environments for their resilience against detection
mechanisms used by malware

## What is it?

**VM detector** is a tool that performs multiple checks on a machine it is running to determine
whether it was executed in a virtual environment. It performs the same checks a legitimate
malware would to identify any potential virtual machine detection vectors. To goal of this program is to
help security researchers have a better understanding of how their machine is
vulnerable to malware detection methods. 

VM-Detector currently supports *VirtualBox* and *VMware* detection.

## Installation

Clone the repository to your local machine:

```commandline
git clone https://github.com/mmianov/VM-detector
```

Install the requirements:

```commandline
pip install -r requirements.txt
```

Navigate to `Flow` directory

```commandline
cd Flow/
```

Run the program:
```commandline
python flow.py
```