import gspread
import json

# I have an key file called service_account.json (its not saved in this Github repo so don't bother)
sa = gspread.service_account()
sh = sa.open("TestingSheets")
wks = sh.worksheet("Sheet1")

with open('posts.json') as f:
    data = json.load(f)

#This works but runtime is very slow and my first instance of running this script gave me an Error 502. Fast internet connection is crucial
for each_item in data:
    row = [each_item["title"]]
    wks.append_row(row)

#Output should be that each row should have an entry from my posts.json file