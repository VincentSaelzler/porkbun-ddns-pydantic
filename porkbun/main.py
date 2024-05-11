import client

# url, json_ = client.generate_get_request("ping")
# response = client.http_post(url, json_)
# public_ip = client.ping(response)

url, json_ = client.generate_get_request("retrieve", "quercusphellos.online")
response = client.http_post(url, json_)
records = client.retrieve(response)
              
                            
# response_bytes = client.get_http("ping", None)
# public_ip = client.get_ip(response_bytes)

# response_bytes = client.get_http("retrieve", "quercusphellos.online")




print("more functional")