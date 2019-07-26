#!/usr/bin/env python

# Domain availability check tool for Gandi API
# https://api.gandi.net/docs/domains/

import requests, json, os, configparser, sys, logging, string, itertools

# curl -X GET 'https://api.gandi.net/v5/domain/check?name=z32.nl' -H 'authorization: Apikey your-api-key'
#    print(json.dumps(r, indent=4, sort_keys=True))

API_URL = 'https://api.gandi.net/v5/'
CHECK_NAME_URL = 'domain/check?name='
ZONE = ['.at', '.be', '.ca', '.cn', '.de', '.dk', '.eu', '.fi', '.fr', '.lt', '.no', '.nz', '.pl',  
        '.pm', '.pw', '.re', '.ro', '.se', '.tf', '.uk', '.wf', '.yt']
# too expensive: im, st
# not possible to register 2 letters: gr, ru, in, li, me, us, za, bz, cc, ch, cz, es, in, li

ALPHABET = list(string.ascii_lowercase) + list(map(str, range(0,10)))
DOMAIN_LENGTH = 2
START_FROM = 'aa.at' #in case script was interrupted
#ALPHABET = ['z', '32', '1']
SCRIPT_NAME_EXT = os.path.splitext(os.path.realpath(__file__))

# LOGGER INIT

logging.basicConfig(
    format='%(asctime)s %(levelname)-5s %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S', 
    level=logging.INFO,
    handlers=[
#        logging.FileHandler(SCRIPT_NAME_EXT[0] + '.log'),
        logging.FileHandler('gandi.log'),
        logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)

#url = 'z32.nl' #test domain

def main():
    logger.info('Script started')
    read_config(SCRIPT_NAME_EXT)

    found = 0
    list_of_all_domains = []
    list_of_domains_to_check = []

    for c in ZONE:
        for _ in list(itertools.product(ALPHABET, repeat=DOMAIN_LENGTH)):
            list_of_all_domains.append(''.join(_) + c)
    
    start = list_of_all_domains.index(START_FROM) + 1
    # start = 0
    # list_of_all_domains = ['9q.at', 'rr.eu']

    for url in list_of_all_domains[start:]:
        print(url + ' - Domains found: ' + str(found))
        response = check_name(url)
        if response:
            found += 1
            logger.info(' Domain: ' + response[0] + ' is available. Price: ' + str(response[1]))
            with open('results.log', 'a') as f:
                f.write(';'.join(response) + '\n')


def check_name(name):
    url = API_URL + CHECK_NAME_URL + name
    logger.debug('Checking domain: ' + name)
    try:
        response = requests.get(url, headers = HEADERS)
    except Exception as e:
        logger.Error('Unable to query name: ' + repr(e) + name)
        return False
    try:
        r = response.json()
    except Exception as e:
        logger.error('Error parsing the request: ' + repr(e) + ' for domain: ' + name)
        return False

    try:
        result = [name, str(r['products'][0]['prices'][0]['price_after_taxes'])]
        return result
    except:
        try:
            logger.info(name + ' - Status: ' + r['products'][0]['status'])
            return False
        except:
            logger.error('Strange behaviour for domain: ' + name)
            return False


def read_config(SCRIPT_NAME_EXT):
    global HEADERS
    config_file = SCRIPT_NAME_EXT[0] + '.cfg'
    config = configparser.ConfigParser()
    config.read(config_file)
    APIKEY = config.get('local', 'apikey')
    HEADERS = {'authorization': 'Apikey ' + APIKEY, 'Content-Type' : 'application/json'}

if __name__ == "__main__":
    main()