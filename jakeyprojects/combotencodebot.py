import json
from datetime import datetime, timezone
from gspread.auth import service_account
from math import fsum

# ✅
class CombotData:
    def __init__(self, combotfile):
        self.combotfile = combotfile
        self.data = None
        self.open()
        self.dates = []
        self.daily_messages = []
        self.hourly_messages = {}
        self.weekday_messages = {"Sunday": 0, "Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0}
        self.ADM = 0
        self.daily_active_users = []
        self.DAU = 0
        self.most_active_hours = []
        self.least_active_hours = []
        self.most_active_day = None
        self.least_active_day = None

    # ✅
    def open(self):
        with open(self.combotfile) as f:
            self.data = json.load(f)

    # ✅
    def format(self):
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

        with open(self.combotfile, 'w') as w:
            json.dump(self.data, w, indent=4)

    # ✅
    class Gather:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.data = None
            self.open()

        def open(self):
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
            self.outer_instance.ADM = int(int(fsum(self.outer_instance.daily_messages))/len(self.outer_instance.daily_messages))

        def get_DAU(self):
            for each_item in self.data["time_series"]:
                self.outer_instance.daily_active_users.append(each_item[2]["active_user_daily"])
            new_DAU = round(int(fsum(self.outer_instance.daily_active_users))/len(self.outer_instance.daily_active_users))
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
            self.get_ADM()
            self.get_DAU()
            self.get_most_hours()
            self.get_least_hours()
            self.get_most_active_day()
            self.get_least_active_day()
            if showdata == True:
                self.showdata()
                
        # ✅
        def showdata(self):
            if self.outer_instance.dates:
                print(self.outer_instance.dates)
            if self.outer_instance.daily_messages:
                print(self.outer_instance.daily_messages)
            if self.outer_instance.ADM:
                print(self.outer_instance.ADM)
            if self.outer_instance.daily_active_users:
                print(self.outer_instance.daily_active_users)
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
    def __init__(self, combotfile, gsheet_name=None, gsheet_worksheet=None, do_format=False):
        super().__init__(combotfile)
        self.auth = service_account()
        self.sh = None
        self.wks = None
        self.var_begin = None
        self.var_end = None
        self.access_gsheet(gsheet_name, gsheet_worksheet)
        self.open()
        if do_format == True:
            self.format()
        self.Gather(self).gather() #Need further revision if things go wrong
        

    # pending 🧑‍💻
    def access_gsheet(self, gsheet_name, gsheet_worksheet):
        self.sh = self.auth.open(gsheet_name)
        self.wks = self.sh.worksheet(gsheet_worksheet)

    # open for tweaking and revisions 👷✅
    # duration is subtracted by 1 for all cases since we are including daybegin and in the iteration
    def start(self, monthbegin, daybegin, duration="weekly", yearbegin=None):
        while True:
            if duration == "monthly":
                if monthbegin in [3, 5, 7, 8, 10]:
                    duration = 30
                    break
                elif monthbegin in [4, 6, 9, 11]:
                    duration = 29
                    break
                elif (monthbegin == 1 and daybegin not in [29,30,31]) or (monthbegin == 12 and isinstance(yearbegin, int) == True and len(str(yearbegin)) == 2) or (monthbegin == 1 and isinstance(yearbegin, int) == True and len(str(yearbegin)) == 2): #additional code to filter some values that don't need yearbegin to proceed
                        duration = 30
                        break
                elif monthbegin == 2 and isinstance(yearbegin, int) == True and len(str(yearbegin)) == 2:
                    if yearbegin % 4 == 0:
                        duration = 28
                        break
                    else:
                        duration = 27
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
                        except ValueError as error:
                            print(error)
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
                duration = 6
                break
            elif duration is None:
                duration = input("Please input 'monthly' or 'weekly': ")
            else:
                duration = input("Error value. Please input 'monthly' or 'weekly': ")

        # assign monthend and dayend considering if dayend overlaps to next month and monthend overlaps to next year
        dayend = daybegin + duration
        if monthbegin == 1:
            if (duration == 6 and daybegin in [26,27,28,29,30,31]) or (duration == 30 and daybegin not in [1,30,31]):
                dayend -= 31 #31 days from Jan.
                monthend = monthbegin + 1
            elif duration == 30 and daybegin in [30,31]:
                monthend = monthbegin + 1
                if yearbegin % 4 == 0:
                    if daybegin == 30:
                        dayend -= 31 #31 days from Jan.
                    elif daybegin == 31:
                        dayend -= 31 + 29 #31 days from Jan. and 29 days from February since we will loop another month
                        monthend += 1
                elif yearbegin % 4 != 0:
                    dayend -= 31 + 28  #31 days from Jan. and 28 days from February
                    monthend += 1
            elif (daybegin <= 25 and duration == 6) or (duration == 30 and daybegin == 1):
                monthend = monthbegin
        elif monthbegin == 2:
            if duration == 6 and daybegin in [23,24,25,26,27,28,29]:
                if yearbegin % 4 == 0 and daybegin > 23:
                    dayend -= 29 #29 days of Feb.
                    monthend = monthbegin + 1
                elif yearbegin % 4 == 0 and daybegin == 23:
                    monthend = monthbegin
                elif yearbegin % 4 != 0:
                    dayend -= 28 #28 days of Feb.
                    monthend = monthbegin + 1
            elif duration in [27,28]:
                dayend -= duration
                monthend = monthbegin + 1
            elif (daybegin <= 22 and duration == 6) or (duration in [27,28] and daybegin == 1):
                monthend = monthbegin
        elif monthbegin == 12:
            if (duration == 6 and daybegin in [26,27,28,29,30,31]) or (duration == 30 and daybegin != 1):
                dayend -= 31 #31 days from Dec.
                monthend = monthbegin - 11 #reset back to january
                yearend = yearbegin + 1
            elif (daybegin <= 25 and duration == 6) or (duration == 30 and daybegin == 1):
                monthend = monthbegin
        else:
            if (monthbegin in [3, 5, 7, 8, 10] and duration == 6 and daybegin in [26,27,28,29,30,31]) or (duration == 30 and daybegin != 1):
                dayend -= 31 #31 days from the months
                monthend = monthbegin + 1
            elif (monthbegin in [4, 6, 9, 11] and duration == 6 and daybegin in [25,26,27,28,29,30]) or (duration == 29 and daybegin != 1):
                dayend -= 30 #30 days from the months
                monthend = monthbegin + 1
            elif (monthbegin in [3, 5, 7, 8, 10] and duration == 6 and daybegin <= 25) or (monthbegin in [4, 6, 9, 11] and duration == 6 and daybegin <= 24) or (duration in [29,30] and daybegin == 1):
                monthend = monthbegin
        if yearbegin:
            self.data_range(monthbegin, daybegin, monthend, dayend, yearbegin)
        else:
            self.data_range(monthbegin, daybegin, monthend, dayend)
        self.total_messages(duration)
        self.average_daily_messages(duration)
        self.active_users(duration)
        self.m_active_hours()
        self.l_active_hours()
        self.m_active_day()
        self.l_active_day()

    #✅
    # CAUTION ⚠️
    # this function can be ran multiple times as long as there is an existing row, if its done without, the last row will be OVERWRITTEN.
    # this function, if ran only once, will update and can append rows if needed without issues.
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
            #print(yearbegin)
        self.var_begin = f"{formatted_monthbegin} {formatted_daybegin}"
        self.var_end = f"{formatted_monthend} {formatted_dayend}"
        entry = f"{formatted_monthbegin} {formatted_daybegin} — {formatted_monthend} {formatted_dayend}"
        #print(self.var_begin, self.var_end)
        if self.var_begin in self.dates and self.var_end in self.dates:
            #print("loading...")
            if number <= self.wks.row_count:
                while cell.value is not None:
                    number += 1
                    notation = f"{letter}{number}"
                    cell = self.wks.acell(notation) if number <= self.wks.row_count else cell
                    if number > self.wks.row_count:
                        break
            #print(f"We have added another entry at row {number}.")
            if number > self.wks.row_count:
                self.wks.add_rows(1)
            notation = f"{letter}{number}"
            cell = self.wks.acell(notation) 
            self.wks.update(notation, entry)
            #print("Done!")
        else:
            print("Beginning or end dates cannot be found.")


    def total_messages(self, duration):
        letter = "B"
        number = 1
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation) 

        index = 0
        for each_date in self.dates:
            if self.var_begin == each_date:
                sum_daily_messages = int(fsum(self.daily_messages[index:index + duration + 1])) # added 1 to make sure the last item is called
            index += 1

        #print("loading...")
        if number <= self.wks.row_count:
            while cell.value is not None:
                number += 1
                notation = f"{letter}{number}"
                cell = self.wks.acell(notation) if number <= self.wks.row_count else cell
                if number > self.wks.row_count:
                    break
        #print(f"We have added another entry at row {number}.")
        if number > self.wks.row_count:
            self.wks.add_rows(1)
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation) 
        self.wks.update(notation, sum_daily_messages)
        #print("Done!")
        
    def average_daily_messages(self, duration):
        letter = "C"
        number = 1
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation)

        index = 0
        for each_date in self.dates:
            if self.var_begin == each_date:
                sum_ADM = int(int(fsum(self.daily_messages[index:index + duration + 1]))/len(self.daily_messages))

        #print("loading...")
        if number <= self.wks.row_count:
            while cell.value is not None:
                number += 1
                notation = f"{letter}{number}"
                cell = self.wks.acell(notation) if number <= self.wks.row_count else cell
                if number > self.wks.row_count:
                    break
        #print(f"We have added another entry at row {number}.")
        if number > self.wks.row_count:
            self.wks.add_rows(1)
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation) 
        self.wks.update(notation, sum_ADM)
        #print("Done!")
    
    def active_users(self, duration):
        letter = "F"
        number = 1
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation)

        index = 0
        for each_date in self.dates:
            if self.var_begin == each_date:
                sum_DAU = round(int(fsum(self.daily_active_users[index:index + duration + 1]))/len(self.daily_active_users))
                #print(sum_DAU)

        #print("loading...")
        if number <= self.wks.row_count:
            while cell.value is not None:
                number += 1
                notation = f"{letter}{number}"
                cell = self.wks.acell(notation) if number <= self.wks.row_count else cell
                if number > self.wks.row_count:
                    break
        #print(f"We have added another entry at row {number}.")
        if number > self.wks.row_count:
            self.wks.add_rows(1)
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation) 
        self.wks.update(notation, sum_DAU)
        #print("Done!")

    # not flexible
    def m_active_hours(self):
        letter = "H"
        number = 1
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation)

        converted_str = ', '.join(self.most_active_hours)

        if number <= self.wks.row_count:
            while cell.value is not None:
                number += 1
                notation = f"{letter}{number}"
                cell = self.wks.acell(notation) if number <= self.wks.row_count else cell
                if number > self.wks.row_count:
                    break
        #print(f"We have added another entry at row {number}.")
        if number > self.wks.row_count:
            self.wks.add_rows(1)
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation) 
        self.wks.update(notation, converted_str)
        #print("Done!")
    
    # not flexible
    def l_active_hours(self):
        letter = "I"
        number = 1
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation)

        converted_str = ', '.join(self.least_active_hours)

        if number <= self.wks.row_count:
            while cell.value is not None:
                number += 1
                notation = f"{letter}{number}"
                cell = self.wks.acell(notation) if number <= self.wks.row_count else cell
                if number > self.wks.row_count:
                    break
        #print(f"We have added another entry at row {number}.")
        if number > self.wks.row_count:
            self.wks.add_rows(1)
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation) 
        self.wks.update(notation, converted_str)
        #print("Done!")
    
    #not flexible
    def m_active_day(self):
        letter = "J"
        number = 1
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation)

        if number <= self.wks.row_count:
            while cell.value is not None:
                number += 1
                notation = f"{letter}{number}"
                cell = self.wks.acell(notation) if number <= self.wks.row_count else cell
                if number > self.wks.row_count:
                    break
        #print(f"We have added another entry at row {number}.")
        if number > self.wks.row_count:
            self.wks.add_rows(1)
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation) 
        self.wks.update(notation, self.most_active_day)
        #print("Done!")

    #not flexible
    def l_active_day(self):
        letter = "K"
        number = 1
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation)

        if number <= self.wks.row_count:
            while cell.value is not None:
                number += 1
                notation = f"{letter}{number}"
                cell = self.wks.acell(notation) if number <= self.wks.row_count else cell
                if number > self.wks.row_count:
                    break
        #print(f"We have added another entry at row {number}.")
        if number > self.wks.row_count:
            self.wks.add_rows(1)
        notation = f"{letter}{number}"
        cell = self.wks.acell(notation) 
        self.wks.update(notation, self.least_active_day)
        print("Done!")

#import threading and os
#for every existing combot file, execute the whole function SIMULTANEOUSLY.