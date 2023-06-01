from gspread.auth import service_account
import json
import time
import threading

starting = time.perf_counter()

url = 'jakeyprojects\health_hero\may2023-hh.json'

with open(url) as combotfile:
    data = json.load(combotfile)

total_msg = []
total_new_user = []
active_user = []
total_user = []

for each in data["time_series"]:
    total_msg.append(each[2]["total_messages_daily"])
    total_new_user.append(each[2]["new_user_daily"])
    active_user.append(each[2]["active_user_daily"])
    total_user.append(each[2]["total_user_daily"])

sa = service_account()
sh = sa.open("Health Hero Community Metrics Report")
wks = sh.worksheet("Telegram")

def encode(column, list):
    letter = column
    number = 126
    notation = f"{letter}{number}"

    for each_item in list:
        wks.update(notation, each_item)
        number += 1
        notation = f"{letter}{number}"


ending = time.perf_counter()
print(f"Elapsed time: {(ending-starting):.4f} seconds")