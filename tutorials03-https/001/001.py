import requests

#HTTP Request to get info from this specific site
response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
#HTTP Response from server in JSON file
json_data = response.json()

print(json_data)
print(type(json_data))

