import model
import os

MOCKFILE_DIR = "porkbun/mockfiles/"
API_KEYS = {"apikey": os.environ["APIKEY"], "secretapikey": os.environ["SECRETAPIKEY"]}

IPV4_ENDPOINT = "https://api-ipv4.porkbun.com/api/json/v3/"


# this variable can change
api_backend: model.Backend
