import requests

url = 'https://jsonplaceholder.typicode.com/users'
url2 = 'https://combot.org/c/1588076288/a/json'
response = requests.get(url)

print(response.text)

#with open('tutorials08-requests/fake.json', 'w') as f:
#    json.dump(data, f, indent=4)
