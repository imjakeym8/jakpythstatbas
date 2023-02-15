# Write a python script that displays the frequency of each number digit inputted by a user.
from collections import Counter

def getlist():
    given_number = input("Number: ")
    my_list = []
    for each_digit in str(given_number):
        my_list.append(int(each_digit)) #Output: [0, 1, 2, 3, 4, ...]
    return my_list

def start():
    number = getlist()
    frequency = Counter(number) #Counter method counts the frequency of the number called.
    print(frequency)

def starthis():
    number = input()
    cnt = Counter(number)
    idk = sorted(cnt)
    for i in idk:
        print(f"{i}: {cnt[i]}", end="")
        if i != idk[-1]:
            print(", ", end="")

start()