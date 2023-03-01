#Given an input number, return the number of times a number performs the ff. until it is 0.
#If even, divide by 2; if odd, subtract by 1.

num = int(input("Number: "))
count = 0
while num > 0:
    count += 1
    if num % 2 == 0:
        num /= 2
    else:
        num -= 1
print(count)