#!/usr/bin/python3
import pathlib
from collections import Counter
import re
import time

RED = '\033[1;31;48m'
WHITE = "\33[0m"
GREEN = '\033[1;32;48m'

#some methods as functions to test on web server Log File :: mainly apache2 web server!

def sort_list(list, ip):
    new_list = []
    for item in list:
        if item not in new_list and item != ip:
            new_list.append(item)
    return new_list
            
def counter_list(sorted_ip_list, data):
    ip_num_list = []
    ip_count = Counter()
    ip_count.update(data.lower().split())
    for ip in sorted_ip_list:
        count_ip = ip_count[f'{ip}']
        ip_num_list.append(f'{ip}:{count_ip}')
    return ip_num_list

def counter_reque(sorted_req_list, full_req):
    req_num_list = []
    for req in sorted_req_list:
         num_count = full_req.count(req)
         req_num_list.append(f'{req}|{num_count}') 
    print(req_num_list)

def frequ_analyse(ip_and_num_list):

    for item in ip_and_num_list:
        address, freq = item.split(":")
        print(f"{RED}{address}{WHITE} has request {GREEN}Frequency{WHITE} {RED}{freq}{WHITE}")
    print("\n")

def mal_ip(log_file, white_ip):
    print(f"[{GREEN}+{WHITE}] scanning {log_file}")
    data = pathlib.Path(log_file).read_text()
    print("\n")
    #print(data)
    list_ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", data)
    sorted_ips = sort_list(list_ips, white_ip)
    print("\n")
    final_ip_num_list = counter_list(sorted_ips, data)
    frequ_analyse(final_ip_num_list)


def list_tup_mal_req(file):
    with open(file, 'r') as log_file:
        full_req_list = []
        for line in log_file.readlines():
            data2 = line.strip()
            req = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \- \- \[.*](.*) HTTP/1.1", data2)
            #print(req[0])
            full_req_list.append(req[0])
    return full_req_list


def mal_req_analysis(file):
    req_tup_num_list = list_tup_mal_req(file)
    for tup_req in req_tup_num_list:
        IP, REQ = tup_req[0], tup_req[1]
        if int(req_tup_num_list.count(tup_req)) > 5:
            print(f"{RED}{IP}{WHITE} → {GREEN}{REQ}{WHITE} {RED}{req_tup_num_list.count(tup_req)}{WHITE} times")
