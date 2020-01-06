import sys, os, subprocess

from testcase_operations import act_test
from testcase_acquisition import make_testcase

def main():
    args = sys.argv
    if not os.path.exists("testcase"):
        subprocess.run(["mkdir", "testcase"])
    code_path = args[1]
    problem = code_path[0]
    if not os.path.exists( os.path.join("testcase", problem)):
        make_testcase(code_path)
    act_test(code_path)
    
if __name__ == '__main__':
    main()

