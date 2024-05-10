import client

# set as tests once a mock api is available
# ip = _get(_post, "ping", "quercusphellos.online")
response_bytes = client.get_http("ping", None)
public_ip = client.validate("ping", response_bytes)

# response_bytes = client.get_http("ping", None)
# records = get("retrieve", "quercusphellos.online")
# records = get("retrieve", None)


print("yay!")