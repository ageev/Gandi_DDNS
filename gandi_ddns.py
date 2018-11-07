#!/usr/bin/env python

# DDNS implementation for Gandi LiveDNS API service

import requests, json, os, configparser, sys

## curl -H"X-Api-Key: $APIKEY" https://dns.api.gandi.net/api/v5/domains/<your_domain>/records/<your_subdomain>/A
## https://doc.livedns.gandi.net/

config_file = "gandi_ddns.cfg"
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def main():
    # step 0. Read config
    global APIKEY, DOMAIN, RECORD, API_URL, CHECKER_URL, STORED_EXTERNAL_IP, HEADERS 
    config = configparser.ConfigParser()
    config.read(config_file)

    APIKEY = config.get('local', 'apikey')
    HEADERS = {'X-Api-Key': APIKEY, 'Content-Type' : 'application/json'}
    DOMAIN = config.get('local', 'domain')
    RECORD = config.get('local', 'record')
    API_URL = config.get('local', 'api_url')
    CHECKER_URL = config.get('local', 'CHECKER_URL')
    STORED_EXTERNAL_IP = config.get('local', 'stored_external_ip')

    # step 1. Get current internet IP from external website
    external_ip = get_external_ip(CHECKER_URL)
    print('External ip: ' + external_ip)

    # step 2. if ip was changed -> goto Gandi and update the record
    if external_ip != STORED_EXTERNAL_IP: 
        set_gandi_ip(DOMAIN, RECORD, external_ip)
        config.set('local', 'stored_external_ip', external_ip)
        with open(config_file, 'w') as configfile:
            config.write(configfile)
            print('[INFO] Config file was updated with new ip')
    else:
        print('[INFO] external ip is still the same. Nothing to update')

# currently not used
# def get_gandi_ip(domain_name, record_name):
#     ''' Get IP from Gandi LiveDNS'''
#     url = API_URL + "domains/" + domain_name + "/records/" + record_name + "/A" 
#     try:
#         response = requests.get(url, headers=HEADERS)
#         result = response.json()[u'rrset_values'][0]
#     except requests.exceptions.HTTPError as e:
#         print('[ERROR] Unable to get external IP address from Gandi: ' +e)
#         sys.exit(2)
#     except json.decoder.JSONDecodeError:
#         print('[ERROR] Json error parsing Gandi server reply')
#         print(response.text)
#         sys.exit(2)

#     return result

def get_external_ip(ip_url):
    try:
        response = requests.get(ip_url)
    except requests.exceptions.HTTPError:
        print('[ERROR] Unable to get external IP address from ' + ip_url)
        sys.exit(2)
    return response.text

def set_gandi_ip(domain_name, record_name, new_ip):
    url = API_URL + "domains/" + domain_name + "/records/" + record_name + "/A"
    body = {'rrset_values': [new_ip,]}
    try:
        response = requests.put(url, headers = HEADERS, json = body)
        print(response.text)
    except requests.exceptions.HTTPError as e:
        print('[ERROR] Unable to change IP: ' + e)

if __name__ == "__main__":
    main()