from porkbun.client import DomainResponse, Record


def get_public_ip():
    return "1.1.1.1"


def get_domain(domain: str):
    match domain:
        case "quercusphellos.online":
            return DomainResponse(
                status="SUCCESS",
                records=[
                    Record(
                        id="000000001",
                        name="quercusphellos.online",
                        type="A",
                        content="1.1.1.1",
                        ttl="600",
                        prio="0",
                        notes=None,
                    ),
                    Record(
                        id="000000002",
                        name="quercusphellos.online",
                        type="NS",
                        content="maceio.porkbun.com",
                        ttl="86400",
                        prio=None,
                        notes=None,
                    ),
                    Record(
                        id="000000003",
                        name="quercusphellos.online",
                        type="NS",
                        content="salvador.porkbun.com",
                        ttl="86400",
                        prio=None,
                        notes=None,
                    ),
                    Record(
                        id="000000004",
                        name="quercusphellos.online",
                        type="NS",
                        content="fortaleza.porkbun.com",
                        ttl="86400",
                        prio=None,
                        notes=None,
                    ),
                    Record(
                        id="000000005",
                        name="quercusphellos.online",
                        type="NS",
                        content="curitiba.porkbun.com",
                        ttl="86400",
                        prio=None,
                        notes=None,
                    ),
                ],
            )
        case _:
            raise NotImplementedError(domain)
