import requests
print(requests.get("http://httpbin.org/ip").json()["origin"])