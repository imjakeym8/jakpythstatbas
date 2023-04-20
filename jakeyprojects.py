import json
from datetime import datetime, timezone, timedelta
from gspread.auth import service_account
from math import fsum

class CombotData:
    def __init__(self, combotfile):
        self.combotfile = combotfile
        self.data = None
        self.dates = []
        self.daily_messages = [] 
        self.hourly_messages = {}
        self.weekdays = {"Sunday": 0, "Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0}
        self.most_active_hours = []
        self.least_active_hours = []
        self.most_active_day = None
        self.least_active_day = None
        
        self.DAU = 0
        self.ADM = 0
        self.maxhour = 0
        self.minhour = 0

        self.hourly_messages1 = []
        self.hourly_messages2 = []

    def __format(self):
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


    def _gather(self): #parameter values should include an option to filter which data should be gathered.
        with open(self.combotfile) as f:
            data = json.load(f)            
        # Days of the data range included
        def get_dates():
            for each_item in data["time_series"]:
                self.dates.append(each_item[0][:8])
            return self.dates

        # Daily Messages of the data range included
        def get_d_messages():
            for each_item in data["time_series"]:
                self.daily_messages.append(each_item[2]["total_messages_daily"])
            return self.daily_messages
            
        # Average Daily Messages of the data range included
        def get_ADM():
            if self.daily_messages == []:
                get_d_messages()
            self.ADM = int(int(fsum(self.daily_messages))/len(self.daily_messages))
            return self.ADM

        # Daily Active Users of the data range included
        def get_DAU():
            list_DAU = []
            for each_item in data["time_series"]:
                list_DAU.append(each_item[2]["active_user_daily"])
            new_DAU = round(int(fsum(list_DAU))/len(list_DAU))
            self.DAU = new_DAU
            return self.DAU

        # Most and Least Active Hours of the data range included
        def get_h_messages():
            for key, value in data["active_hours"].items():
                self.hourly_messages[key] = value
                self.hourly_messages1.append(value)
                self.hourly_messages2.append(value)
            self.maxhour = max(list(self.hourly_messages.values()))
            self.minhour = min(list(self.hourly_messages.values()))
            return self.hourly_messages

        def sort_hour(hour):
                return datetime.strptime(hour, '%I:%M %p')
            
        def get_most_hours():
            if self.maxhour == 0:
                get_h_messages()
            while len(self.most_active_hours) != 3:
                for key, value in data["active_hours"].items():
                    if self.maxhour == value and len(self.most_active_hours) != 3:
                        self.most_active_hours.append(key)
                        self.hourly_messages1.remove(value)   
                        self.maxhour = max(self.hourly_messages1)
            sorted_max = sorted(self.most_active_hours, key=sort_hour)
            self.most_active_hours = sorted_max
            return self.most_active_hours     

        def get_least_hours():
            if self.minhour == 0:
                get_h_messages()
            while len(self.least_active_hours) != 3:
                for key, value in data["active_hours"].items():
                    if self.minhour == value and len(self.least_active_hours) != 3:
                        self.least_active_hours.append(key)
                        self.hourly_messages2.remove(value)   
                        self.minhour = min(self.hourly_messages2)
            sorted_min = sorted(self.least_active_hours, key=sort_hour)
            self.least_active_hours = sorted_min
            return self.least_active_hours

        #Most and Least Active Days of the data range included
        def get_wd_messages():
            for each_item in data["time_series"]:
                for each_day in self.weekdays.keys():
                    if each_item[1] == each_day:
                        self.weekdays[each_day] = each_item[2]["total_messages_daily"] + self.weekdays[each_day]
            weekdays_messages = list(self.weekdays.values())
            self.most_active_day = max(weekdays_messages)
            self.least_active_day = min(weekdays_messages)
            
            for key, each_day in self.weekdays.items():
                if each_day == self.most_active_day:
                    return f"{key} is the most active day with {self.most_active_day} messages."
                if each_day == self.least_active_day:
                    return f"{key} is the least active day with {self.least_active_day} messages."

        print(get_dates())
        print(get_d_messages())
        print(get_ADM())
        print(get_DAU())
        print(get_h_messages())
        print(get_most_hours())
        print(get_least_hours())
        print(get_wd_messages())           
       
class GsheetEncoder(CombotData):
    def __init__(self):
        super().__init__()
        self.auth = service_account()

    def access_gsheet(self, gsheet_name, gsheet_worksheet):
        self.sh = self.auth.open(gsheet_name)
        self.wks = self.sh.worksheet(gsheet_worksheet)

    def data_range(self, monthbegin, daybegin, duration, monthend=None, dayend=None):
        self.monthbegin = monthbegin
        self.daybegin = daybegin
        if duration % 7 != 0:
            raise ValueError("Invalid duration value.")
        self.duration = duration
        self.monthend = monthend
        self.dayend = dayend    

file = 'copy.json'
jsoncombot = CombotData(file)

print(jsoncombot._gather())
