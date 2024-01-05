import requests

BASE = "http://127.0.0.1:5000/"

# response = requests.get(BASE + "helloworld/tim/19")
# response = requests.post(BASE + "helloworld")
response = requests.get(BASE + "helloworld/bill")
print(response.json())



