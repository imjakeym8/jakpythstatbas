import json
from datetime import datetime, timezone

url = 'copy.json'

# FORMAT FUNCTION
def format(url):
    with open(url) as f:
        data = json.load(f)

        # 1. access the key of each active_hours ✅
        # 2. convert timestamp to datetime object ✅
        # 3. format it to 00:00 AM - 11:00 PM ✅
        # 4. create a new dictionary and replace it with the dictionary inside "active_hours" ✅
        new_dict = {}
        for key, value in data["active_hours"].items():
            hour_min = key
            hour_min += ":00"
            hour_12 = datetime.strptime(hour_min, '%H:%M')
            formatted_time = hour_12.strftime('%I:%M %p')
            new_dict[formatted_time] = value
        data["active_hours"] = new_dict

        # 1. remove last 3 digits of timestamp ✅
        # 2. convert timestamp to datetime object ✅
        # 3. format it using strftime  ✅
        for each_item in data["time_series"]:
            str_item = str(each_item[0])[:10]
            unix = datetime.fromtimestamp(int(str_item), tz=timezone.utc)
            formatted_day = unix.strftime('%B %d %Y')
            each_item[0] = formatted_day
            each_item[1]["active_user_daily"] = each_item[1].pop("a")            
            each_item[1]["new_user_daily"] = each_item[1].pop("n")        
            each_item[1]["total_user_daily"] = each_item[1].pop("s")        
            each_item[1]["total_messages_daily"] = each_item[1].pop("m")

    with open(url, 'w') as w:
        json.dump(data, w, indent=4)

# GATHER FUNCTION
def gather(url):
    with open (url) as f:
        json.load()
