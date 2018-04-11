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


def is_server_respond_with_200(url):
    try:
        response = requests.get(url)
        return response.ok
    except ValueError:
        return False


def get_domain_expiration_date(domain_name):
    try:
        domain_info = whois.query(domain_name)
        return domain_info.expiration_date
    except AttributeError:
        return None


def check_expiration_date(expiration_date):
    try:
        delta = expiration_date - datetime.now()
        return delta
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
    args = parse_arguments()
    if not os.path.exists(args.path):
        sys.exit('Path does not exist')
    filepath = args.path
    url_list = load_urls_from_file(filepath)
    for url in url_list:
        domain_name = get_domain_name(url)
        status_code = is_server_respond_with_200(url)
        exp_date = get_domain_expiration_date(domain_name)
        if not status_code or not exp_date:
            print('Domain: | {} | is not healthy'.format(domain_name))
            print('-----------------------------------------')
        else:
            delta_time = check_expiration_date(exp_date)
            if delta_time >= timedelta(30):
                print('Domain: | {} | healthy and expire in {}'.format(
                    domain_name,
                    delta_time)
                )
                print('-----------------------------------------')
