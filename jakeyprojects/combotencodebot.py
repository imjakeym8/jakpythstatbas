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

    # ✅ working 99.9%
    def start(self, monthbegin, daybegin, duration="weekly", yearbegin=None):
        while True:
            if duration == "monthly":
                if monthbegin in [3, 5, 7, 8, 10] and daybegin != 31:
                    duration = 31
                    break
                if monthbegin in [3, 5, 7, 8, 10] and daybegin == 31:
                    while True:
                        try:
                            daybegin = int(input("You can't get 31 days starting from March 31st. Please input another starting day: "))
                            if (daybegin >= 31) or (isinstance(daybegin, int) == False):
                                raise ValueError("Nope. That's not it.")
                            break
                        except ValueError as error:
                            print(error)
                elif monthbegin in [4, 6, 9, 11]:
                    duration = 30
                    break
                elif (monthbegin == 1 and daybegin not in [29,30,31]) or (monthbegin == 12 and isinstance(yearbegin, int) == True and len(str(yearbegin)) == 2) or (monthbegin == 1 and isinstance(yearbegin, int) == True and len(str(yearbegin)) == 2):
                        duration = 31
                        break
                elif monthbegin == 2 and isinstance(yearbegin, int) == True and len(str(yearbegin)) == 2:
                    if yearbegin % 4 == 0:
                        duration = 29
                        break
                    else:
                        duration = 28
                        break
                else:
                    while True:
                        try:
                            yearbegin = int(input("Please add a year value (YY): "))
                            if len(str(yearbegin)) != 2 and isinstance(yearbegin, int) == False:
                                raise ValueError("Please make sure the value is YY.")
                            elif len(str(yearbegin)) != 2 or isinstance(yearbegin, int) == False:
                                raise ValueError("Please make sure the value is YY.")
                            break
                        except ValueError as error2:
                            print(error2)
            elif duration == "weekly":
                if monthbegin == 2 and isinstance(yearbegin, int) == False and len(str(yearbegin)) != 2:
                    while True:
                        try:
                            yearbegin = int(input("Please add a year value (YY): "))
                            if (len(str(yearbegin)) != 2 and isinstance(yearbegin, int) == False) or (len(str(yearbegin)) != 2) or (isinstance(yearbegin, int) == False):
                                raise ValueError("Please make sure the value is YY.")
                            break
                        except ValueError as error2:
                            print(error2)
                duration = 7
                break
            elif duration is None:
                duration = input("Please input 'monthly' or 'weekly': ")
            else:
                duration = input("Error value. Please input 'monthly' or 'weekly': ")

        # assign monthend and dayend considering if dayend overlaps to next month and monthend overlaps to next year
        dayend = daybegin + duration
        if monthbegin == 1:
            if (duration == 7 and daybegin in [25,26,27,28,29,30,31]) or (duration == 31 and daybegin not in [29,30,31]):
                dayend -= 31 #31 days from Jan.
                monthend = monthbegin + 1
            elif duration == 31 and daybegin in [29,30,31]:
                if yearbegin % 4 == 0:
                    dayend -= 29 #29 days from February (leap year)
                    monthend = monthbegin + 1
                    if daybegin > 29:
                        dayend -= duration
                        monthend += 1
                    else:
                        dayend = daybegin
                else:
                    dayend -= duration + 28  #28 days from February
                    monthend = monthbegin + 2
            else:
                monthend = monthbegin
        elif monthbegin == 2:
            if duration == 7 and daybegin in [22,23,24,25,26,27,28,29]:
                if yearbegin % 4 == 0 and daybegin > 22:
                    dayend -= 29
                    monthend = monthbegin + 1
                elif yearbegin % 4 == 0 and daybegin == 22:
                    monthend = monthbegin
                elif yearbegin % 4 != 0:
                    dayend -= 28
                    monthend = monthbegin + 1
            elif duration == 28 or duration == 29:
                dayend -= duration
                monthend = monthbegin + 1
            else:
                monthend = monthbegin
        elif monthbegin == 12:
            if (duration == 7 and daybegin in [25,26,27,28,29,30,31]) or (duration == 31):
                dayend -= 31
                monthend = monthbegin - 11 #reset back to january
                yearend = yearbegin + 1
            else:
                monthend = monthbegin
        else:
            if (monthbegin in [3, 5, 7, 8, 10] and duration == 7 and daybegin in [25,26,27,28,29,30,31]) or (duration == 31):
                dayend -= 31
                monthend = monthbegin + 1
            elif (monthbegin in [4, 6, 9, 11] and duration == 7 and daybegin in [24,25,26,27,28,29,30]) or (duration == 30):
                dayend -= 30
                monthend = monthbegin + 1
            else:
                monthend = monthbegin
        if yearbegin:
            self.data_range(monthbegin, daybegin, monthend, dayend, yearbegin)
        else:
            self.data_range(monthbegin, daybegin, monthend, dayend)

    #✅
    def data_range(self, monthbegin, daybegin, monthend, dayend, yearbegin=None):
        letter = "A"
        number = 1
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation)

        dt_monthbegin = datetime.strptime(str(monthbegin), '%m')
        dt_daybegin = datetime.strptime(str(daybegin), '%d')
        dt_monthend = datetime.strptime(str(monthend), '%m')
        dt_dayend = datetime.strptime(str(dayend), '%d')
        formatted_monthbegin = dt_monthbegin.strftime('%B')         
        formatted_daybegin = dt_daybegin.strftime('%d')         
        formatted_monthend = dt_monthend.strftime('%B') 
        formatted_dayend = dt_dayend.strftime('%d')         
        if yearbegin is not None:
            dt_year = datetime.strptime(str(yearbegin), '%y')
            formatted_year = dt_year.strftime('%y')
            print(yearbegin)
        var_begin = f"{formatted_monthbegin} {formatted_daybegin}"
        var_end = f"{formatted_monthend} {formatted_dayend}"
        entry = f"{formatted_monthbegin} {formatted_daybegin} — {formatted_monthend} {formatted_dayend}"
        if var_begin in self.dates and var_end in self.dates:
            print("loading...")
            if number <= self.wks.row_count:
                while cell.value is not None:
                    number += 1
                    if number > self.wks.row_count:
                        break
                if number > self.wks.row_count:
                    self.wks.add_rows(1)
                notation = f"{letter}{number}"
                cell = self.wks.acell(notation) 
                self.wks.update(notation, entry)
                print("Done!")
        else:
            print("Beginning or end dates cannot be found.")
        

url = 'jakeyprojects/blphcopy.json'
cd = CombotData(url)
ge = GsheetEncoder(url, "TestingSheets", "Manual")
ic = ge.Gather(ge)
ic.gather()
ge.start(3, 4, 'weekly')