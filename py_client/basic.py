import requests
#endpoint= "https://httpbin.org/status/200/"
#endpoint="https://httpbin.org/anything"
endpoint="http://localhost:8000/"

get_response=requests.get(endpoint, params={"abc":123})  # HTTP request

print(get_response.text)

print(get_response.json())
print(get_response.status_code)






