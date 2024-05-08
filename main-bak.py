from pydantic import BaseModel
from sys import argv
from datetime import datetime, UTC
import subprocess
import requests


class Log(BaseModel):
    timestamp: datetime
    success: bool
    ip_addr: str
    domains: list[str]
    message: str

class PostData(BaseModel):
    apikey: str
    secretapikey: str




def main(domains: list[str]):



        
    for d in domains:
        
        r = requests.post(f"{BASE_ENDPOINT}/retrieve/{d}", key_json)
        print()
        
        
        # get the currrent root host record

        # if public ip mismatches root host record, upsert
        pass

        # domain_names
        # print("in main")


if __name__ == "__main__":

    # assumptions and incoming argurments
    LOG_FILE = "ddns-log.json"
    KEY_FILE = "porkbun-keys.json"
    BASE_ENDPOINT = "https://porkbun.com/api/json/v3/dns"
    start_timestamp = datetime.now(UTC)
    domains = argv[1:]  # skip first argument (name of the script)
    domains = ["quercusphellos.online"]

    # initialize output log record
    log = Log(
        timestamp=start_timestamp,
        success=True,
        ip_addr="",
        domains=domains,
        message="",
    )

    try:
        # confirm incoming data is valid
        if len(domains) == 0:
            raise ValueError("specify at least one domain name")

        # update dns records
        main(domains)

    except Exception as e:

        # generate debug info
        log.success = False
        log.message = str(e)

    finally:

        # log latest run
        with open(LOG_FILE, "w") as file:
            file.write(log.json())
