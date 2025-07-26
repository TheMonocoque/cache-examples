#!/usr/bin/env python

import requests

server_url = "http://localhost:8000"

# Initial request to get resource and ETag
response = requests.get(server_url + "/resource")

print("Initial Response:")
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print(f"Content: {response.text}")
    etag = response.headers["ETag"]
    local_etags = {"resource": etag}
else:
    local_etags = {}

# Subsequent request with If-None-Match header
headers = {"If-None-Match": local_etags.get("resource")} if local_etags else {}
response = requests.get(server_url + "/resource", headers=headers)

print("\nSecond Request:")
print(f"Status Code: {response.status_code}")
if response.status_code == 304:
    print("No content returned (cache still valid)")
else:
    print("New content received")
    local_etags["resource"] = response.headers.get("ETag")
