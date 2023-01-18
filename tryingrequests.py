import requests
import time

r = requests.get('https://xkcd.com/353/')

print(r.text)
print("hello")
print(time.perf_counter())