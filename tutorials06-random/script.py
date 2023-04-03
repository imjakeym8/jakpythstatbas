data = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700] #23 elements found.
weekdays = {"Sunday": 0, "Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0}


weeks = len(data) / 7
min_days = int(weeks) * 7
diff = len(data) - min_days
increment = 0

# Convert dictionary to a list, that way i can return any key from a dictionary given the index
listed_weekdays = list(weekdays.keys())

for i in range(int(weeks)+1):
    for num, value in enumerate(weekdays.keys()):
        weekdays[listed_weekdays[num]] = weekdays.get(listed_weekdays[num]) + data[num + increment]
        if i == 3 and num+increment == len(data)-1 and len(data) % 7 != 0:
            break
    increment += 7

for key, value in weekdays.items():
    print(key, value)

