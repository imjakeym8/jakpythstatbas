import json
import gspread
import math
from datetime import datetime

# -- FILE MANAGEMENT SECTION --
# Downloaded a fresh copy of my JSON file in this specific directory
#with open('tutorials05-gspread/20123-22823.json') as j:
#    combot = json.load(j)
#
#
#with open('tutorials07-json/file.json', 'w') as f:
#   json.dump(combot, f, indent=3)

with open('tutorials07-json/file.json') as raw_data:
    combot_dict = json.load(raw_data)

#for each_value in combot_dict["active_hours"].values():
#    print(each_value)

# Updated the old keys with new comprehensive keys
#for i in combot_dict["time_series"]:
#    i[1]["active_user_daily"] = i[1].pop("a")
#    i[1]["new_user_daily"] = i[1].pop("n")
#    i[1]["total_user_daily"] = i[1].pop("s")
#    i[1]["total_messages_daily"] = i[1].pop("m")

#with open('tutorials07-json/file.json', 'w') as raw_data:
#    json.dump(combot_dict, raw_data, indent=3)

# -- PARSING DATA SECTION --
active_users = []
for each_day in combot_dict["time_series"]:
    active_users.append(each_day[1]["active_user_daily"])

hours_data = []
for each_hour in combot_dict["active_hours"].values():
    hours_data.append(each_hour)

days_data = []
for each_date in combot_dict["time_series"]:
    days_data.append(each_date[1]["total_messages_daily"])

f_total_messages = combot_dict.get("total_messages") #Output: 9327 (maybe w/o stickers or GIFs) 
f_active_users = combot_dict.get("active_users") #Output: 564
f_DAU = combot_dict.get("daily_users") #Output: 50
f_ADM = combot_dict.get("daily_messages") #Output: 333

weekday_data = {"Monday":1228,"Tuesday":1260,"Wednesday":1098,"Thursday":1192,"Friday":1289,"Saturday":1287,"Sunday":1215} #Total is 8569, NOT SAME
total_hours_data = int(math.fsum(hours_data)) #Output: 9327, SAME
total_active = int(math.fsum(active_users)) #Output: 1387, NOT SAME
total_days_data = int(math.fsum(days_data)) #Output: 9327, SAME

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# GOOGLE SHEETS CREATION

sa = gspread.service_account()
sh = sa.open("TestingSheets")
wks = sh.worksheet("Manual")
#sh.add_worksheet(title="Combot Integration Test", rows=4, cols=10)

#worksheet = sh.worksheet("Combot Integration Test")

# -- COMPUTATION SECTION --

# R = 1
# C = 1
# for each_item in months:
#     wks.update_cell(R, C, each_item)
#     R += 1

## wks.format("A2:A13", {
##     'verticalAlignment': 'MIDDLE',
##     'horizontalAlignment': 'CENTER',
##     'textFormat': {
##         'fontFamily': 'Default (Arial)'
##     }
## })

# STRING FORMATTING SECTION

xxx = datetime.fromtimestamp(1675296000)

print(xxx)