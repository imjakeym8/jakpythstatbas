import json

with open('tutorials05-gspread/20123-22823.json') as f:
    dict = json.load(f)
    dict['remarks'] = {}
    new_dict = json.dumps(dict, indent=2)

print(new_dict)

# my_dict = {"old_key": "value"}
# my_dict["new_key"] = my_dict.pop("old_key")
# print(my_dict) would now have an output: {"new_key": "value"}

