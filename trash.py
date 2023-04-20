import json
from datetime import datetime, timezone
from math import fsum

url = 'copy.json'

# FORMAT FUNCTION
def format(url):
    with open(url) as f:
        data = json.load(f)

        new_dict = {}
        for key, value in data["active_hours"].items():
            hour_min = key
            hour_min += ":00"
            hour_12 = datetime.strptime(hour_min, '%H:%M')
            formatted_time = hour_12.strftime('%I:%M %p')
            new_dict[formatted_time] = value
        data["active_hours"] = new_dict
        
        for each_item in data["time_series"]:
            str_item = str(each_item[0])[:10]
            unix = datetime.fromtimestamp(int(str_item), tz=timezone.utc)
            formatted_day = unix.strftime('%B %d %Y')
            formatted_weekday = unix.strftime('%A')
            each_item[0] = formatted_day
            each_item[1]["active_user_daily"] = each_item[1].pop("a")            
            each_item[1]["new_user_daily"] = each_item[1].pop("n")        
            each_item[1]["total_user_daily"] = each_item[1].pop("s")        
            each_item[1]["total_messages_daily"] = each_item[1].pop("m")
            each_item.insert(1, formatted_weekday)

    with open(url, 'w') as w:
        json.dump(data, w, indent=4)

# GATHER FUNCTION
def gather(url, excludeData=None):
    with open(url) as f:
        data = json.load(f)

    dates = []
    daily_messages = []
    hourly_messages = {}
    weekdays = {"Sunday": 0, "Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0}

    ADM = 0 # for the daily messages inside the data range, refer to [messages]
    DAU = 0
    maxhour = 0
    minhour = 0
    hourly_messages_copy1 = []
    hourly_messages_copy2 = []
    most_active_hours = []
    least_active_hours = []

    # Days of the data range included
    def get_dates():
        for each_item in data["time_series"]:
            dates.append(each_item[0][:8])
        return dates

    # Daily Messages of the data range included
    def get_d_messages():
        for each_item in data["time_series"]:
            daily_messages.append(each_item[2]["total_messages_daily"])
        return daily_messages
        
    # Average Daily Messages of the data range included
    def get_ADM():
        if daily_messages == []:
            get_d_messages()
        ADM = int(int(fsum(daily_messages))/len(daily_messages))
        return ADM

    # Daily Active Users of the data range included
    def get_DAU():
        list_DAU = []
        for each_item in data["time_series"]:
            list_DAU.append(each_item[2]["active_user_daily"])
        new_DAU = round(int(fsum(list_DAU))/len(list_DAU))
        DAU = new_DAU
        return DAU

    # Most and Least Active Hours of the data range included
    def get_h_messages():
        for key, value in data["active_hours"].items():
            hourly_messages[key] = value
            hourly_messages_copy1.append(value)
            hourly_messages_copy2.append(value)
        maxhour = max(list(hourly_messages.values()))
        minhour = min(list(hourly_messages.values()))
        return hourly_messages

    def sort_hour(hour):
            return datetime.strptime(hour, '%I:%M %p')
    
    def get_most_hours():
        if maxhour == 0:
            get_h_messages()
        while len(most_active_hours) != 3:
            for key, value in data["active_hours"].items():
                if maxhour == value and len(most_active_hours) != 3:
                    most_active_hours.append(key)
                    hourly_messages_copy1.remove(value)   
                    maxhour = max(hourly_messages_copy1)
        sorted_max = sorted(most_active_hours, key=sort_hour)
        most_active_hours = sorted_max
        return most_active_hours     

    def get_least_hours():
        if minhour == 0:
            get_h_messages()
        while len(least_active_hours) != 3:
            for key, value in data["active_hours"].items():
                if minhour == value and len(least_active_hours) != 3:
                    least_active_hours.append(key)
                    hourly_messages_copy2.remove(value)   
                    minhour = min(hourly_messages_copy2)
        sorted_min = sorted(least_active_hours, key=sort_hour)
        least_active_hours = sorted_min
        return least_active_hours

    #Most and Least Active Days of the data range included
    def get_wd_messages():
        for each_item in data["time_series"]:
            for each_day in weekdays.keys():
                if each_item[1] == each_day:
                    weekdays[each_day] = each_item[2]["total_messages_daily"] + weekdays[each_day]
        weekdays_messages = list(weekdays.values())
        most_active_day = max(weekdays_messages)
        least_active_day = min(weekdays_messages)

        for key, each_day in weekdays.items():
            if each_day == most_active_day:
                return f"{key} is the most active day with {most_active_day} messages."
            if each_day == least_active_day:
                return f"{key} is the least active day with {least_active_day} messages."

    if excludeData == None:
        print(get_dates())
        print(get_d_messages())
        print(get_ADM())
        print(get_DAU())
        print(get_h_messages())
        print(get_most_hours())
        print(get_least_hours())
        print(get_wd_messages())

print(gather(url))