import json
from datetime import datetime, timezone
from gspread.auth import service_account
from math import fsum

# ✅
class CombotData:
    def __init__(self, combotfile):
        self.combotfile = combotfile
        self.data = None
        self.__open()

    # ✅
    def __open(self):
        with open(self.combotfile) as f:
            self.data = json.load(f)

    # ✅
    def _format(self):
        new_dict = {}
        for key, value in self.data["active_hours"].items():
            hour_min = key
            hour_min += ":00"
            hour_12 = datetime.strptime(hour_min, '%H:%M')
            formatted_time = hour_12.strftime('%I:%M %p')
            new_dict[formatted_time] = value
        self.data["active_hours"] = new_dict
        
        for each_item in self.data["time_series"]:
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
            json.dump(self.data, w, indent=4)

    # ✅
    class CombotDataDetails:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.data = None
            self.__open()
            self.dates = []
            self.daily_messages = []
            self.hourly_messages = {}
            self.weekday_messages = {"Sunday": 0, "Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0}
            self.ADM = 0
            self.DAU = 0
            self.most_active_hours = []
            self.least_active_hours = []
            self.most_active_day = None
            self.least_active_day = None
            

        def __open(self):
            with open(self.outer_instance.combotfile) as f:
                self.data = json.load(f)

        def get_dates(self):
            for each_item in self.data["time_series"]:
                self.dates.append(each_item[0][:8])

        def get_d_messages(self):
            for each_item in self.data["time_series"]:
                self.daily_messages.append(each_item[2]["total_messages_daily"])

        def get_ADM(self):
            if self.daily_messages == []:
                self.get_d_messages()
            self.ADM = int(int(fsum(self.daily_messages))/len(self.daily_messages))

        def get_DAU(self):
            list_DAU = []
            for each_item in self.data["time_series"]:
                list_DAU.append(each_item[2]["active_user_daily"])
            new_DAU = round(int(fsum(list_DAU))/len(list_DAU))
            self.DAU = new_DAU

        def get_h_messages(self):
            for key, value in self.data["active_hours"].items():
                self.hourly_messages[key] = value

        def sort_hour(self, hour):    
                return datetime.strptime(hour, '%I:%M %p')
        
        # Note that max/min may not consider if there are two or more arguments that are largest/smallest in amount
        def get_most_hours(self):
            if self.hourly_messages == {}:
                self.get_h_messages()
            listed_h_messages = list(self.hourly_messages.values())
            maxhour = max(listed_h_messages)
            while len(self.most_active_hours) != 3:
                for key, value in self.data["active_hours"].items():
                    if maxhour == value and len(self.most_active_hours) != 3:
                        self.most_active_hours.append(key)
                        listed_h_messages.remove(value)
                        maxhour = max(listed_h_messages)
            sorted_max = sorted(self.most_active_hours, key=self.sort_hour)
            self.most_active_hours = sorted_max

        def get_least_hours(self):
            if self.hourly_messages == {}:
                self.get_h_messages()
            listed_h_messages = list(self.hourly_messages.values())
            minhour = min(listed_h_messages)
            while len(self.least_active_hours) != 3:
                for key, value in self.data["active_hours"].items():
                    if minhour == value and len(self.least_active_hours) != 3:
                        self.least_active_hours.append(key)
                        listed_h_messages.remove(value)   
                        minhour = min(listed_h_messages)
            sorted_min = sorted(self.least_active_hours, key=self.sort_hour)
            self.least_active_hours = sorted_min
        
        def get_wd_messages(self):
            for each_item in self.data["time_series"]:
                for each_day in self.weekday_messages.keys():
                    if each_item[1] == each_day:
                        self.weekday_messages[each_day] = each_item[2]["total_messages_daily"] + self.weekday_messages[each_day]

        def get_most_active_day(self):
            if int(fsum(list(self.weekday_messages.values()))) == 0:
                self.get_wd_messages() 
            weekdays_messages = list(self.weekday_messages.values())
            most_active_day_messages = max(weekdays_messages)
            for key, each_day in self.weekday_messages.items():
                if each_day == most_active_day_messages:
                    self.most_active_day = key

        def get_least_active_day(self):
            if int(fsum(list(self.weekday_messages.values()))) == 0:
                self.get_wd_messages()
            weekdays_messages = list(self.weekday_messages.values())
            least_active_day_messages = min(weekdays_messages)
            for key, each_day in self.weekday_messages.items():
                if each_day == least_active_day_messages:
                    self.least_active_day = key

        # Please add an option parameter to filter what not to gather ✍️
        def gather(self, showdata=None):
            self.get_dates()
            self.get_d_messages()
            self.get_h_messages()
            self.get_wd_messages()
            self.get_ADM
            self.get_DAU
            self.get_most_hours()
            self.get_least_hours()
            self.get_most_active_day()
            self.get_least_active_day()
            while True:
                showdata = input("Show data? Y or N? ")
                if showdata == 'Y':
                    self.showdata()
                    break
                elif showdata == 'N':
                    break
                else:
                    print("Invalid input.")         

        # ✅
        def showdata(self):
            if self.dates:
                print(self.dates)
            if self.daily_messages:
                print(self.daily_messages)
            if self.ADM:
                print(self.ADM)
            if self.hourly_messages:
                print(self.hourly_messages)
            if self.most_active_hours:
                print(self.most_active_hours)
            if self.least_active_hours:
                print(self.least_active_hours)
            if self.weekday_messages:
                print(self.weekday_messages)            
            if self.most_active_day:
                print(self.most_active_day)
            if self.least_active_day:
                print(self.least_active_day)            

# 🚧👷🚧
class GsheetEncoder(CombotData):
    def __init__(self, combotfile):
        super().__init__()
        self.combotfile = combotfile
        self.auth = service_account()
        self.sh = None
        self.wks = None
        #self.access_gsheet(gsheet_name, gsheet_worksheet)

    # pending 🧑‍💻
    def access_gsheet(self, gsheet_name, gsheet_worksheet):
        self.sh = self.auth.open(gsheet_name)
        self.wks = self.sh.worksheet(gsheet_worksheet)

    def data_range(self, monthbegin=1, daybegin=1):
        innerclass = self.CombotDataDetails(self)
        str_month = str(monthbegin)
        str_day = str(daybegin)
        month_dt = datetime.strptime(str_month, '%m')
        formatted_month = month_dt.strftime('%B')
        day_dt = datetime.strptime(str_day, '%d')
        formatted_day = day_dt.strftime('%d')
        var_date = f"{formatted_month} {formatted_day}"
        dates_dict = dict(zip(innerclass.dates, innerclass.daily_messages))
        for key, value in dates_dict.items():
            if key == var_date:
                print("Good!")
            


url = 'jakeyprojects/blphcopy.json'
cd = CombotData(url)
ic = cd.CombotDataDetails(cd)
ic.gather()
ge = GsheetEncoder(url)
ge.data_range(3, 31)


