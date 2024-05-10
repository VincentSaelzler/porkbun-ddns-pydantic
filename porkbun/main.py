import client

# set as tests once a mock api is available
# ip = _get(_post, "ping", "quercusphellos.online")
ip = client._get(_post, "ping", None)
# records = get("retrieve", "quercusphellos.online")
# records = get("retrieve", None)