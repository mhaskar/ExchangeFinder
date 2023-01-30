import argparse
from threading import Thread
from core.functions import *

show_banner()

parser = argparse.ArgumentParser(description='DNSStager main parser')

parser.add_argument(
    '--domain',
    required=False,
    help='The target domain you want to scan (example.com)'
)

parser.add_argument(
    '--domains',
    required=False,
    help='Path to domains file you want to scan (domains.txt)'
)

parser.add_argument(
    '--useragent',
    required=False,
    help='Useragent to use, the default is "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36."'
)

parser.add_argument(
    '--output',
    required=False,
    help='Export results to given .csv file'
)


parser.add_argument(
    '--verbose',
    required=False,
    help='Show detailed output',
    action='store_true'
)


args = parser.parse_args()

domain = args.domain
domains_file = args.domains
verbose = args.verbose
useragent = args.useragent
output_file = args.output


if output_file:
    create_output_file_headers(output_file)


if useragent is None:
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36."

def exchange_finder_domain(sub_domains_list):
    for subdomain in sub_domains_list:
        if verbose:
            scanning_message = "\t Checking host %s" % (subdomain)
            print_note(scanning_message)
        ip = resolve_A_records(subdomain)
        if ip:
            port = check_https_open(str(ip))
            if port:
                domain_to_check = "https://%s" % subdomain
                check_exchange_header(domain_to_check, useragent, output_file)
            else:
                if verbose:
                    error_find_https_hosts_message = "\tCan't find web server on (%s:443)" % subdomain
                    print_note(error_find_https_hosts_message)   
                else:
                    pass
        else:
            if verbose:
                error_find_active_hosts_message = "\tCan't resolve host (%s)" % subdomain
                print_note(error_find_active_hosts_message)
            else:
                pass
        



if domain is None and domains_file is None:
    print_error("Please use --domain or --domains option")
    exit()

if domain is not None and domains_file is not None:
    print_error("Please select an option --domain or --domains, you can't use both!")
    exit()

if domain:
    scanning_single_domain_message = "Scanning domain %s" % domain
    print_note(scanning_single_domain_message)
    get_mx_records_domain(domain)
    domains = generate_domains(domain)
    exchange_finder_domain(domains)

if domains_file:
    file_status = check_domains_file(domains_file)
    if file_status:
        fi = open(domains_file, "r")
        domains_content = [domain.strip("\n") for domain in fi.readlines()]
        if len(domains_content) > 1:
            domains_count_message = "Total domains to scan are {0} domains".format(len(domains_content))
            print_sucess(domains_count_message)
        elif len(domains_content) == 1:
            domains_count_message = "Scanning 1 domain only".format(len(domains_content))
            print_sucess(domains_count_message)
        elif len(domains_content) == 0:
            domains_count_zero_message = "No domains found in target domains file"
            print_error(domains_count_zero_message)
        for single_domain in domains_content:
            scanning_domain_from_file_message = "Scanning domain %s" % single_domain
            print_note(scanning_domain_from_file_message)
            get_mx_records_domain(single_domain)

            subdomains_multi_domains = generate_domains(single_domain)
            main_domain_thread = Thread(target=exchange_finder_domain, args=(subdomains_multi_domains, ))
            main_domain_thread.start()
            main_domain_thread.join()

    else:
        domains_file_not_found_message = "Target domains file %s not found!" % domains_file
        print_error(domains_file_not_found_message)
        exit()        





