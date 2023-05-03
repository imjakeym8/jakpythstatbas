def january_add(day, leap=False):
    # ASSUMING THAT I WANT TO ADD MONTHLY BY 31 DAYS
    if leap == True:
        leap = 29
    else:
        leap = 28

    answer = day + 31 #no. of total days
    total_days = "Number of days right now: {}"

    if leap == 29:
        if day > leap:
            final = day - leap
            monthwday = "What is the day? March {}"
        else:
            final = day
            monthwday = "What is the day? February {}"
    else:
        final = day - leap
        monthwday = "What is the day? March {}" 

    print(total_days.format(answer))
    print(monthwday.format(final))
    print("---")

#january_add(29,True)  #Output should be February 29
#january_add(30,True)  #Output should be March 1
#january_add(31,True)  #Output should be March 2
#january_add(29,False)  #Output should be March 1 
#january_add(30,False)  #Output should be March 2
#january_add(31,False)  #Output should be March 3

monthbegin = 1
daybegin = 29
duration = 31
yearbegin = 24

dayend = daybegin + duration
if monthbegin == 1:
    if (duration == 7 and daybegin in [25,26,27,28,29,30,31]) or (duration == 31 and daybegin not in [29,30,31]):
        dayend -= 31 #31 days from Jan.
        monthend = monthbegin + 1
    elif duration == 31 and daybegin in [29,30,31]:
        if yearbegin % 4 == 0:
            print(dayend)
            dayend -= 29 #29 days from February (leap year)
            monthend = monthbegin + 1
            print(f"ok {monthend}/{dayend}")
            if daybegin != 29:
                monthend += 1