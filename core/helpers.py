#!/usr/bin/python

import os
from termcolor import cprint

def print_sucess(text):
    message = "[+] %s" % text
    cprint(message, "green")


def print_error(text):
    message = "[-] %s" % text
    cprint(message, "red")


def print_note(text):
    message = "[!] %s" % text
    cprint(message, "yellow")


def print_results(domain, redirected_login_page, exchange_version, iss_version):

    message = "\tDomain Found : %s\n" % domain
    message+= "\t\033[1mExchange version : %s\n" % exchange_version
    message+= "\tLogin page : %s\n" % redirected_login_page
    message+= "\tIIS/Webserver version: %s\n"  % iss_version

    cprint(message, "green")


def print_mx_records(records):

    message = "\t[+] The following MX records found for the main domain\n"
    for record in records:
        message+= "\t\033[1m" + str(record) + "\n"
    cprint(message, "green")


def create_output_file_headers(output_file):
    f = open(output_file, "w")
    headers = "domain, login_page, exchange_version, web_server_version\n"
    f.write(headers)
    f.close()


def save_results(output_file, domain, redirected_login_page, exchange_version, web_server_version):
    f = open(output_file, "a")
    content = "{0},{1},{2},{3}\n".format(domain, redirected_login_page, exchange_version, web_server_version)
    f.write(content)
    f.close()    


def check_domains_file(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False


def show_banner():
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

    banner = r'''
    {0}
    ______     __                           _______           __         
   / ____/  __/ /_  ____ _____  ____ ____  / ____(_)___  ____/ /__  _____
  / __/ | |/_/ __ \/ __ `/ __ \/ __ `/ _ \/ /_  / / __ \/ __  / _ \/ ___/
 / /____>  </ / / / /_/ / / / / /_/ /  __/ __/ / / / / / /_/ /  __/ /    
/_____/_/|_/_/ /_/\__,_/_/ /_/\__, /\___/_/   /_/_/ /_/\__,_/\___/_/     
                             /____/                                        
                                                {1}
                                                {2}Find that Microsoft Exchange server ..{1}
    '''.format(OKBLUE, ENDC, OKGREEN)

    print(banner)