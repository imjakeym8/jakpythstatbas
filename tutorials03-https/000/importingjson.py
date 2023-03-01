import json

with open('combot-a.json') as f:
    data = json.load(f)

for x in data["time_series"]:
    del x[0]

with open('combot-b.json', 'w') as f:
    json.dump(data, f, indent=1)

