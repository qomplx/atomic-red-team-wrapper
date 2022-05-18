import subprocess
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from argparse import ArgumentParser

load_dotenv()

ATOMIC_PATH=os.getenv('INVOKE-ATOMIC')
POWERSHELL_LIST = ['pwsh', 'powershell.exe']
POWERSHELL = 'pwsh'

# Ensure that output path is there...
def dir_check():
    if not os.path.isdir('output'):
        print("=== Directories Created ===")
        os.mkdir('output')
    else:
        pass
    return

# Load test list from file...
def load_tests(file):
    tests = None

    with open(file, 'r') as f:
        tests = f.read().splitlines()

    f.close()

    return tests

# Write output to output directory...
def write_to_file(out_location, data):
    try:
        with open(f'output/{out_location}-{datetime.now()}.txt', 'a') as of:
            of.write(data)

        return True
    except Exception as e:

        print("=== Data Failed to Write Output ===")
        print(e)

        return False

# Input check to see if the detection works...
def not_a_shell():

    nas = input("\n\n(C) Continue, (R) Retry >>> ")

    if nas.upper() == "C" or nas.upper() == "R":
        print("\n\n\n")
        return nas.upper()
    else:
        print("Bad input...")
        not_a_shell()

# Do a test on a remote machine...
def start_remote_session():

    #$sess = New-PSSession -ComputerName testcomputer -Credential domain\username



    return True

# Do the red team tests...
def run_tests(list, cp=None, out_location=None, ex=None):
    if ex is None:
        ex = POWERSHELL

    for test in list:
        time = datetime.now().strftime("%Y-%m-%d%H%M%S").replace("\s", "-")
        if cp is not False:
            print(f"=== Running Test: {test} ===")
            p = subprocess.Popen(f"{ex} -command 'Import-Module {ATOMIC_PATH}; Invoke-AtomicTest {test} -PromptForInputArgs *>&1 | Tee-Object output/{out_location}_{test}_{time}.txt'", shell=True)
            p.communicate()
            p.kill()
            print(f"===========================")

            check = not_a_shell()

            if check == "R":
                retry = [test]
                run_tests(retry, cp=cp, out_location=out_location, ex=ex)
            else:
                pass

        else:
            print(f"=== Running Test: {test} ===")

            p = subprocess.Popen(f"{ex} -command 'Import-Module {ATOMIC_PATH}; Invoke-AtomicTest {test} *>&1 | Tee-Object output/{out_location}_{test}_{time}.txt'", shell=True)
            p.communicate()
            p.kill()
            print(f"===========================")


            check = not_a_shell()

            if check == "R":
                retry = [test]
                run_tests(retry, cp, out_location=out_location, ex=ex)
            else:
                pass

    return True


def main():
    dir_check()

    parser = ArgumentParser(description="Purple Team Wrapper using Atomic Red Team (Invoke-AtomicTest)")

    parser.add_argument('-l', '--list', help="List of tests to be tested")
    parser.add_argument('-cp', '--custom-parameters', help="Enable custom parameters", action='store_true')
    parser.add_argument('-o', '--output', help="stdin to file output")
    parser.add_argument('-e', '--executable', help="powershell executable (default: pwsh)")

    args = parser.parse_args()

    if args.list and args.output:
        tests=load_tests(args.list)
        run_tests(list=tests, cp=args.custom_parameters, out_location=args.output, ex=args.executable)
        print("=== Testing Completed ===")
    else:
        print("=== Please give a list (-l, --list) of MITRE ATT&CK tasks to test and output name (-o, --output) === \n\n=== Help (-h) ===")


if __name__ == '__main__':
    main()
