import os

MOCKFILE_DIR = "porkbun/mockfiles/"
API_KEYS = {"apikey": os.environ["APIKEY"], "secretapikey": os.environ["SECRETAPIKEY"]}

IPV4_ENDPOINT = "https://api-ipv4.porkbun.com/api/json/v3"
DNS_ENDPOINT = "https://porkbun.com/api/json/v3/dns"


