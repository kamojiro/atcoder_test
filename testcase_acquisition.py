import subprocess, sys, os, csv
from collections import defaultdict

import requests, lxml
from bs4 import BeautifulSoup

import config

def login():
    login_url = "https://atcoder.jp/login"
    session = requests.session()
    login_html = session.get(login_url)
    login_lxml = BeautifulSoup(login_html.text, 'lxml')
    csrf_token = login_lxml.find( attrs = {'name': 'csrf_token'}).get('value')

    login_info = {
        "csrf_token": csrf_token,
        "username": config.USERNAME,
        "password": config.PASSWORD
    }

    login_result = session.post(login_url, data=login_info)
    login_result.raise_for_status()

    return session

def get_problem_html(problem_url):
    session = requests.get(problem_url)
    if session.status_code == 200:
        return session
    return login().get(problem_url)


def make_testcase(code_path):
    d = defaultdict(lambda : "")
    d["beginner"] = "abc"
    d["regular"] = "arc"
    d["grand"] = "agc"
    
    pwd = list( map( lambda x:x.strip(), subprocess.run("pwd", stdout=subprocess.PIPE, text=True).stdout.split("/")))
    problem_number = code_path.split('/')[-1][0]
    problem_number_small = chr( ord("a") + ord(problem_number) - ord("A"))
    contest_name = d[ pwd[-2]] + pwd[-1]
    problem_url = os.path.join("https://atcoder.jp/contests/", contest_name, "tasks", contest_name+"_"+problem_number_small)

    problem_html = get_problem_html(problem_url)
    problem_lxml = BeautifulSoup(problem_html.text, 'lxml')
    samples = [ a.text.strip().split("\r\n") for a in problem_lxml.find_all('pre')]
    if problem_lxml.find('span', class_="lang-en") == None:
        number_of_samples = len(samples)//2
    else:
        number_of_samples = len(samples)//4
    if number_of_samples == 0:
        print("Login failed or No authentification")
        exit(1)

    testcase_path = os.path.join("testcase", code_path[0])
    subprocess.run(["mkdir", testcase_path])
    testcase_in_path = os.path.join(testcase_path, "in")
    testcase_out_path = os.path.join(testcase_path, "out")
    subprocess.run(["mkdir", testcase_in_path])
    subprocess.run(["mkdir", testcase_out_path])
    for i in range(number_of_samples):
        # print("sample", i+1)
        # print("\n".join(samples[i*2+1]))
        # print("\n".join(samples[i*2+2]))
        # print("")
        with open( os.path.join(testcase_in_path, str(i+1)+".txt"), mode='w') as f:
            f.write("\n".join(samples[i*2+1]))
        with open( os.path.join(testcase_out_path, str(i+1)+".txt"), mode='w') as f:
            f.write("\n".join(samples[i*2+2]))
