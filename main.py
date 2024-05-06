from pydantic import BaseModel
from sys import argv
from datetime import datetime, UTC


class Log(BaseModel):
    timestamp: datetime
    success: bool
    ip_addr: str
    domains: list[str]
    message: str


def main(domain_names: list[str]):
    # p = Person(fn="v", ln="s")

    # file_path = "person.json"
    # with open(file_path, "w") as file:
    #     file.write(p.json())
    print("in main")


if __name__ == "__main__":
    
    LOG_FILE = "ddns-log.json"

    # log the start time
    # now_str = datetime.now(UTC).isoformat()
    start_timestamp = datetime.now(UTC)

    # get incoming args (list of domain names)
    # skip the first argument (name of the script)
    domain_names = argv[1:]

    o = Log(
        timestamp=start_timestamp,
        success=True,
        ip_addr="",
        domains=domain_names,
        message="",
    )

    try:
        main(domain_names)
        raise Exception("whoops")
    except Exception as e:
        o.success = False
        o.message = str(e)
    finally:
        # log latest run
        with open(LOG_FILE, "w") as file:
            file.write(o.json())
