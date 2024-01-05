import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes":75,"name":"Joe","views":100000},
		{"likes":10,"name":"Tim","views":20000},
		{"likes":67,"name":"Rest Api Tutorial","views":8000}]

for i in range(len(data)):
	response = requests.put(BASE + "video/" + str(i), data[i])
	print(response.json())


input()
response = requests.delete(BASE + 'video/0')
print(response)

input()
response = requests.get(BASE + 'video/2')
print(response.json())

