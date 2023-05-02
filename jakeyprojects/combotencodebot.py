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
    class Gather:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.data = None
            self.__open()

        def __open(self):
            with open(self.outer_instance.combotfile) as f:
                self.data = json.load(f)

        def get_dates(self):
            for each_item in self.data["time_series"]:
                self.outer_instance.dates.append(each_item[0][:8])

        def get_d_messages(self):
            for each_item in self.data["time_series"]:
                self.outer_instance.daily_messages.append(each_item[2]["total_messages_daily"])

        def get_ADM(self):
            if self.outer_instance.daily_messages == []:
                self.get_d_messages()
            self.outer_instance.ADM = int(int(fsum(self.daily_messages))/len(self.outer_instance.daily_messages))

        def get_DAU(self):
            list_DAU = []
            for each_item in self.data["time_series"]:
                list_DAU.append(each_item[2]["active_user_daily"])
            new_DAU = round(int(fsum(list_DAU))/len(list_DAU))
            self.outer_instance.DAU = new_DAU

        def get_h_messages(self):
            for key, value in self.data["active_hours"].items():
                self.outer_instance.hourly_messages[key] = value

        def sort_hour(self, hour):
                return datetime.strptime(hour, '%I:%M %p')

        # Note that max/min may not consider if there are two or more arguments that are largest/smallest in amount
        def get_most_hours(self):
            if self.outer_instance.hourly_messages == {}:
                self.get_h_messages()
            listed_h_messages = list(self.outer_instance.hourly_messages.values())
            maxhour = max(listed_h_messages)
            while len(self.outer_instance.most_active_hours) != 3:
                for key, value in self.data["active_hours"].items():
                    if maxhour == value and len(self.outer_instance.most_active_hours) != 3:
                        self.outer_instance.most_active_hours.append(key)
                        listed_h_messages.remove(value)
                        maxhour = max(listed_h_messages)
            sorted_max = sorted(self.outer_instance.most_active_hours, key=self.sort_hour)
            self.outer_instance.most_active_hours = sorted_max

        def get_least_hours(self):
            if self.outer_instance.hourly_messages == {}:
                self.get_h_messages()
            listed_h_messages = list(self.outer_instance.hourly_messages.values())
            minhour = min(listed_h_messages)
            while len(self.outer_instance.least_active_hours) != 3:
                for key, value in self.data["active_hours"].items():
                    if minhour == value and len(self.outer_instance.least_active_hours) != 3:
                        self.outer_instance.least_active_hours.append(key)
                        listed_h_messages.remove(value)
                        minhour = min(listed_h_messages)
            sorted_min = sorted(self.outer_instance.least_active_hours, key=self.sort_hour)
            self.outer_instance.least_active_hours = sorted_min

        def get_wd_messages(self):
            for each_item in self.data["time_series"]:
                for each_day in self.outer_instance.weekday_messages.keys():
                    if each_item[1] == each_day:
                        self.outer_instance.weekday_messages[each_day] = each_item[2]["total_messages_daily"] + self.outer_instance.weekday_messages[each_day]

        def get_most_active_day(self):
            if int(fsum(list(self.outer_instance.weekday_messages.values()))) == 0:
                self.get_wd_messages()
            weekdays_messages = list(self.outer_instance.weekday_messages.values())
            most_active_day_messages = max(weekdays_messages)
            for key, each_day in self.outer_instance.weekday_messages.items():
                if each_day == most_active_day_messages:
                    self.outer_instance.most_active_day = key

        def get_least_active_day(self):
            if int(fsum(list(self.outer_instance.weekday_messages.values()))) == 0:
                self.get_wd_messages()
            weekdays_messages = list(self.outer_instance.weekday_messages.values())
            least_active_day_messages = min(weekdays_messages)
            for key, each_day in self.outer_instance.weekday_messages.items():
                if each_day == least_active_day_messages:
                    self.outer_instance.least_active_day = key

        # Please add an option parameter to filter what not to gather ✍️
        def gather(self, showdata=False):
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
            if showdata == True:
                self.showdata()
#            while True:
#                showdata = input("Show data? Y or N? ")
#                if showdata == 'Y':
#                    self.showdata()
#                    break
#                elif showdata == 'N':
#                    break
#                else:
#                    print("Invalid input.")

        # ✅
        def showdata(self):
            if self.outer_instance.dates:
                print(self.outer_instance.dates)
            if self.outer_instance.daily_messages:
                print(self.outer_instance.daily_messages)
            if self.outer_instance.ADM:
                print(self.outer_instance.ADM)
            if self.outer_instance.DAU:
                print(self.outer_instance.DAU)
            if self.outer_instance.hourly_messages:
                print(self.outer_instance.hourly_messages)
            if self.outer_instance.most_active_hours:
                print(self.outer_instance.most_active_hours)
            if self.outer_instance.least_active_hours:
                print(self.outer_instance.least_active_hours)
            if self.outer_instance.weekday_messages == {'Sunday': 0, 'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0}:
                pass
            else:
                print(self.outer_instance.weekday_messages)
            if self.outer_instance.most_active_day:
                print(self.outer_instance.most_active_day)
            if self.outer_instance.least_active_day:
                print(self.outer_instance.least_active_day)

# 🚧👷🚧
class GsheetEncoder(CombotData):
    def __init__(self, combotfile, gsheet_name=None, gsheet_worksheet=None):
        super().__init__(combotfile)
        self.auth = service_account()
        self.sh = None
        self.wks = None
        self.access_gsheet(gsheet_name, gsheet_worksheet)

    # pending 🧑‍💻
    def access_gsheet(self, gsheet_name, gsheet_worksheet):
        self.sh = self.auth.open(gsheet_name)
        self.wks = self.sh.worksheet(gsheet_worksheet)

    def data_range(self, monthbegin, daybegin, duration=None, yearbegin=None):
        while True:
            if duration == "monthly":
                if monthbegin in [1, 3, 5, 7, 8, 10, 12]:
                    duration = 31
                    break
                elif monthbegin in [4, 6, 9, 11]:
                    duration = 30
                    break
                elif monthbegin == 2 and isinstance(yearbegin, int) == True and len(str(yearbegin)) == 2:
                    if yearbegin % 4 == 0:
                        duration = 29
                        break
                    else:
                        duration = 28
                        break
                else:
                    try:
                        yearbegin = int(input("Please add a year value (YY): "))
                        if len(str(yearbegin)) != 2 and isinstance(yearbegin, int) == False:
                            raise ValueError("Please make sure the value is YY.")
                        elif len(str(yearbegin)) != 2 or isinstance(yearbegin, int) == False:
                            raise ValueError("Please make sure the value is YY.")
                    except ValueError:
                        print("Invalid input. Please enter a valid year value.")
            elif duration == "weekly":
                if monthbegin == 2 and isinstance(yearbegin, int) == False and len(str(yearbegin)) != 2:
                    try:
                        yearbegin = int(input("Please add a year value (YY): "))
                        if len(str(yearbegin)) != 2 and isinstance(yearbegin, int) == False:
                            raise ValueError("Please make sure the value is YY.")
                        elif len(str(yearbegin)) != 2 or isinstance(yearbegin, int) == False:
                            raise ValueError("Please make sure the value is YY.")
                    except ValueError:
                        print("Invalid input. Please enter a valid year value.")
                duration = 7
                break
            elif duration is None:
                duration = input("Please input 'monthly' or 'weekly': ")
            else:
                duration = input("Error value. Please input 'monthly' or 'weekly': ")
        print(monthbegin, daybegin, duration, yearbegin)

#        if monthbegin == 2 and yearbegin is None:
#            print("Please add year")
#        elif monthbegin == 2 and yearbegin is not None:
#            if yearbegin % 4 == 0: # counting only leap years from 2000-2099
#                if daybegin in [24,25,26,27,28,29]:
#                    dayend = daybegin + duration - 29
#                else:
#                    dayend = daybegin + duration
#            monthend = monthbegin + 1
#        elif monthbegin == 12:
#            if daybegin in [26,27,28,29,30,31]:
#                dayend = 

#        entry = ""
#        dt_month = datetime.strptime(str(monthbegin), '%m')
#        dt_day = datetime.strptime(str(daybegin), '%d')
#        formatted_month = dt_month.strftime('%B')
#        formatted_day = dt_day.strftime('%d')
#        if yearbegin is not None:
#            dt_year = datetime.strptime(str(yearbegin), '%y')
#            formatted_year = dt_year.strftime('%y')
#        var_date = f"{formatted_month} {formatted_day}"
#        for each_day in self.dates:
#            if var_date == each_day:
#                entry += f"{var_date}"
#                print(f"{entry} lol")
#                print(formatted_day)

        

url = 'jakeyprojects/blphcopy.json'
cd = CombotData(url)
ge = GsheetEncoder(url, "TestingSheets", "Manual")
ic = ge.Gather(ge)
ic.gather()
ge.data_range(2, 28)