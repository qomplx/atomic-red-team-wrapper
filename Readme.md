# AtomicRedTeam Purple Team Wrapper
----
Small wrapper to use Invoke-AtomicRedTeam in Purple Team Engagements.

We had a situation where we wanted to have multiple MITRE attack detections
tested to ensure that detections were working correctly. There was also a need
for having different toolsets in the environment tested that detections were
being written and implemented in.

Thus this tool was written to give red teamers and blue teamers a way to test
a certain set of MITRE techniques against a device.


At this time only local tests are implemented with more development to come for
handling remote sessions at a later date.

## Installation
----

Ensure powershell is on the device:

Linux
https://docs.microsoft.com/en-us/powershell/scripting/install/install-ubuntu?view=powershell-7.2

MacOS
`brew install powershell`

Install Invoke-AtomicRedTeam via powershell:

https://github.com/redcanaryco/invoke-atomicredteam

Install Python requirements...
`$ pip3 install -r requirements.txt`


Setup Environment Variable

`$ cp .env.example .env`

`INVOKE-ATOMIC="<PATH to psd1 here>"`


# Usage
---

```
$ python3 main.py -h
usage: main.py [-h] [-l LIST] [-cp] [-o OUTPUT] [-e EXECUTABLE]

Purple Team Wrapper using Atomic Red Team (Invoke-AtomicTest)

optional arguments:
 -h, --help            show this help message and exit
 -l LIST, --list LIST  List of tests to be tested
 -cp, --custom-parameters
                       Enable custom parameters
 -o OUTPUT, --output OUTPUT
                       stdin to file output
 -e EXECUTABLE, --executable EXECUTABLE
                       powershell executable (default: pwsh

```

`example-list.txt`
```
T1040
T1003
```

Run Tests with default arguments:

`$ python3 main -l example-list.txt -o example`

Run Tests with custom parameters:

`$ python3 main -l example-list.txt -o example -cp`

All output will be saved in the `./output` directory that will be created on first run
of the tool.

EX: `./output/example_T1040_2022-05-18093142.txt`
