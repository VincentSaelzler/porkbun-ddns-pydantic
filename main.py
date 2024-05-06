from pydantic import BaseModel
from sys import argv
from datetime import datetime, UTC


class Person(BaseModel):
    fn: str
    ln: str


def main(domain_names: list[str]):
    # p = Person(fn="v", ln="s")

    # file_path = "person.json"
    # with open(file_path, "w") as file:
    #     file.write(p.json())
    print("in main")


if __name__ == "__main__":

    # log the start time
    now_str = datetime.now(UTC).isoformat()

    # get incoming args (list of domain names)
    # skip the first argument (name of the script)
    domain_names = argv[1:]

    try:
        main(domain_names)
    except Exception as e:
        # create a file to log and debug failures
        file_path = "DDNS-FAILURE.txt"
        with open(file_path, "w") as file:
            file.write(now_str + "\n" + str(e))
