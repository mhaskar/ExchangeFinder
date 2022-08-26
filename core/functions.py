#!/usr/bin/python3

import dns.resolver
import requests
import warnings
import socket
from .exchange_versions import *
from .helpers import *


warnings.filterwarnings('ignore', message='Unverified HTTPS request')


def get_mx_records_domain(domain):
    mx_records = resolve_MX_records(domain)
    if mx_records:
        print_mx_records(mx_records)
    else:
        print_error("No MX records found (%s)!" % domain)


def resolve_MX_records(domain):
    try:
        response = dns.resolver.resolve(domain, "MX")
        mxs = [mx for mx in response]
        return mxs

    except Exception as e:
        return False


def generate_domains(domain):

    f = open("core/subdomains.txt", "r")
    data = f.readlines()
    subdomains = ["%s.%s" % (subdomain.strip("\n"), domain) for subdomain in data]

    return(subdomains)


def resolve_A_records(domain):
    try:
        response = dns.resolver.resolve(domain, "A")
        for ip in response:
            return ip

    except Exception as e:
        return False


def check_https_open(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    results = sock.connect_ex((ip, 443))
    if results == 0:
        return True
    else:
        return False


def check_exchange_header(domain, user_agent, output_file):

    request_headers = {
        "User-Agent": user_agent
    }

    checking_owa_message = "\tScanning host (%s)" % domain.split("https://")[1]
    print_note(checking_owa_message)
    domain_with_owa = domain + "/owa/"
    req = requests.get(domain, verify=False, headers=request_headers)
    owa_status_code = req.status_code
    if owa_status_code != 200:
        print_error("\t The path /owa/ not found (%s)" % domain)
    else:
        headers = req.headers
        if "Server" in headers.keys():
                
                web_server_version = headers["Server"]
                if "IIS" in web_server_version:
                    iis_message = "\tIIS server detected (%s)" % domain
                    print_sucess(iis_message)
                else:
                    web_server_message = "\tWebserver %s detected (%s)" % (web_server_version, domain)
                    print_sucess(web_server_message)
                req2 = requests.get(domain_with_owa, verify=False, allow_redirects=False, headers=request_headers)
                status_code = req2.status_code
                headers_request2 = req2.headers
                if status_code == 302:
                    print_note("\tPotential Microsoft Exchange Identified")

                    if "X-OWA-Version" in headers_request2.keys() and "Location" in headers_request2.keys():
                        owa_version = headers_request2["X-OWA-Version"]
                        exchange_version = get_exchange_version(owa_version)
                        redirected_login_page = headers_request2["Location"]

                    elif "X-OWA-Version" not in headers_request2.keys() and "Location" in headers_request2.keys():
                        exchange_version = "Not Detected"
                        redirected_login_page = headers_request2["Location"]

                    print_sucess("\tMicrosoft Exchange identified with the following details:\n")  
                    print_results(domain, redirected_login_page, exchange_version, web_server_version)
                    if output_file is not None:
                        save_results(output_file, domain, redirected_login_page, exchange_version, web_server_version)
                
                elif status_code == 404:
                    not_found_message = "\tThe path /owa/ not found (%s)" % domain_with_owa
                    print_note(not_found_message)
                
                elif status_code == 200 and "X-OWA-Version" not in headers_request2.keys() and "Location" not in headers_request2.keys():
                    owa_path_found_but_not_for_exchange = "\tThe path /owa/ found but Microsoft Exchange wasn't identified (%s)" % domain_with_owa
                    print_note(owa_path_found_but_not_for_exchange)
