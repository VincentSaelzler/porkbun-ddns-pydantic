import client





public_ip = client.get_public_ip()

# url, json_ = client.generate_http_request("retrieve", "quercusphellos.online")
# response = client.http_post(url, json_)
# records = client.retrieve(response)

# url, json_ = client.generate_set_request(
#     "editByNameType", "quercusphellos.online", records[0]
# )
# response = client.http_post(url, json_)


# url, json_ = client.generate_set_request(
#     "editByNameType", "quercusphellos.online", records[1]
# )


# response = client.http_post(url, json_)
# response_bytes = client.get_http("ping", None)
# public_ip = client.get_ip(response_bytes)

# # response_bytes = client.get_http("retrieve", "quercusphellos.online")


print("more functional")
