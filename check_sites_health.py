import whois
import argparse
import os
import requests
import sys
from datetime import datetime, timedelta
from urllib.parse import urlparse


def load_urls_from_file(filepath):
    try:
        with open(filepath, 'r') as file:
            url_list = file.read().splitlines()
        return url_list
    except ValueError:
        return None


def get_domain_name(url):
    domain_name = urlparse(url).netloc
    return domain_name


def is_server_respond_with_ok(url):
    try:
        response = requests.get(url)
        return response.ok
    except ValueError:
        return False


def get_domain_expiration_date(domain_name):
    try:
        domain_info = whois.query(domain_name)
        if isinstance(domain_info.expiration_date, list):
            return domain_info.expiration_date[0]
        else:
            return domain_info.expiration_date
    except TypeError:
        return None


def check_expiration_date(expiration_date, days_count):
    current_date = datetime.now()
    try:
        return bool((
                        expiration_date - current_date) > timedelta(days_count)
                    )
    except ValueError:
        return None


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
    days_count = 30
    args = parse_arguments()
    if not os.path.exists(args.path):
        sys.exit('Path does not exist')
    filepath = args.path
    url_list = load_urls_from_file(filepath)
    for url in url_list:
        domain_name = get_domain_name(url)
        status_code = is_server_respond_with_ok(url)
        exp_date = get_domain_expiration_date(domain_name)
        paid_for_month = check_expiration_date(exp_date, days_count)
        print('-----------------------------------------')
        print('Domain {}'.format(domain_name))
        print('Is it respond OK?: {}'.format(status_code))
        if paid_for_month:
            print('Domain is paid for month')
        else:
            print('Domain is not paid for month')
        print('-----------------------------------------')
