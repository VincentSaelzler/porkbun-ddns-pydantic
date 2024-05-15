# need to borrow private methods from client
# pyright: reportPrivateUsage=false

from client import PorkbunRecord, Request, Response, _generate_set_request
from model import Record


def get_public_ip():
    return "69.69.69.69"


def get_records(domain: str):
    match domain:
        case "quercusphellos.online":
            return [
                PorkbunRecord(
                    id="399347448",
                    name="quercusphellos.online",
                    type="A",
                    content="137.220.108.97",
                ),
                PorkbunRecord(
                    id="399348596",
                    name="www.quercusphellos.online",
                    type="CNAME",
                    content="quercusphellos.online",
                ),
            ]

        case _:
            raise NotImplementedError()


def _mock_post(request: Request):
    print(
        request.model_dump_json(indent=2, exclude={"body": {"apikey", "secretapikey"}})
    )


def create_record(domain: str, record: Record):
    request = _generate_set_request("create", domain, record)
    _mock_post(request)
    return Response(status="SUCCESS")
