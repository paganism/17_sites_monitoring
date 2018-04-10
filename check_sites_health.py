import whois
import argparse
import os
import requests
import sys
from datetime import datetime
from datetime import timedelta


def load_urls_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            url_list = file.read().splitlines()
        return url_list
    except ValueError:
        return False


def is_server_respond_with_200(url):
    try:
        status_code = requests.get(url).status_code
        return status_code
    except ValueError:
        return None


def get_domain_expiration_date(domain_name):
    try:
        domain_info = whois.query(domain_name)
        return domain_info.expiration_date
    except ValueError:
        return None


def check_expiration_date(expiration_date):
    delta = expiration_date - datetime.now()
    return delta


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        dest='path',
        required=True,
        help='Path to file'
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    if not os.path.exists(args.path):
        sys.exit('Path does not exist')
    filepath = args.path
    url_list = load_urls_from_file(filepath)
    for url in url_list:
        status_code = (is_server_respond_with_200(url))
        if status_code:
            exp_date = (get_domain_expiration_date(url))
            delta = check_expiration_date(exp_date)
        print('Domain: {} has status code {} and expire in {}'.format(url, status_code, delta))
