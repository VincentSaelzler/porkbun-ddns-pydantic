from typing import Any


# with open("porkbun/mockfiles/xxx.json", "wb") as fout:
#     fout.write(r.content)def post(url: str, json: dict[str, Any]):


def _get_content(endpoint: str):
    DIR = "porkbun/mockfiles/"
    path = DIR + endpoint + ".json"
    with open(path, "rb") as f:
        return f.read()


def post(url: str, json: dict[str, Any]):
    match url:
        case "https://api-ipv4.porkbun.com/api/json/v3/ping":
            return _get_content("ping")
        case _:
            raise NotImplemented(url)
