# testcase/
# └── A
#     ├── in
#     │   ├── 1.txt
#     │   └── 2.txt
#     └── out
#         ├── 1.txt
#         └── 2.txt


import os, subprocess
from collections import Counter, defaultdict

def text_match(a, b):
    a_list = list( a.strip().split('\n'))
    b_list = list( b.strip().split('\n'))
    if len(a_list) != len(b_list):
        return False
    for i in range( len(a_list)):
        if a_list[i].strip() != b_list[i].strip():
            return False
    return True

def test_code(code_path, testcase_path, expectedcase_path):
    p = subprocess.Popen(["cat", testcase_path], stdout=subprocess.PIPE)
    answer = subprocess.run( ["python", code_path], stdin=p.stdout, stdout=subprocess.PIPE, text=True).stdout
    p.stdout.close()
    with open(expectedcase_path) as f:
        expectedcase = f.read()
    if text_match(answer, expectedcase):
        return True, None
    else:
        return False, answer

def act_test(code_path):
    problem_number = code_path.split('/')[-1][0]
    testdirectory_path = os.path.join('testcase', problem_number)
    testcase_path = os.path.join(testdirectory_path, 'in')
    expectedcase_path = os.path.join(testdirectory_path, 'out')
    ls_samples = 'ls -l ' + testcase_path
    number_of_samples = Counter(subprocess.run(ls_samples.split(), stdout=subprocess.PIPE, text=True).stdout)['\n']
    OK = "\033[33mOK\033[0m"
    NG = "\033[31mNG\033[0m"
    cnt = 0
    for i in range(1, number_of_samples):
        collectness, wrong = test_code(code_path, os.path.join(testcase_path, str(i)+".txt"), os.path.join(expectedcase_path, str(i)+".txt"))
        if collectness:
            print(i, OK)
            cnt += 1
        else:
            print(i, NG)
            print(wrong.strip())
    print("----------")
    if cnt == number_of_samples-1:
        print(OK, "{}/{}".format(cnt, number_of_samples-1))
    else:
        print(NG, str(cnt)+"/"+str(number_of_samples-1))




    
    
    
    

