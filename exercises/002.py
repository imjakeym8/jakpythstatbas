#Check how many times a given number can be divided by 3 before it is less than or equal to 10

def mydivide3():
    count = 0
    given_number = int(input("Number: "))
    if abs(given_number) <= 10 and abs(given_number) % 3 == 0:
        while abs(given_number) >= 1:
            count += 1
            given_number = given_number/3
            if abs(given_number) >= 1:
                print("..divided by 3, you get", given_number)
            else:
                count -= 1
                print("Done. It took", count,"times to divide before your number reaches 1 or below.")
    elif abs(given_number) > 10 and abs(given_number) % 3 == 0:
        while abs(given_number) > 10:
            count += 1
            given_number = given_number/3
            if abs(given_number) > 10:
                print("..divided by 3, you get", given_number)
            else:
                count -= 1
                print("Done. It took", count,"times to divide before your number reaches 10 or below.")
    else:
        print("Your number is not divisible by 3. Run the script again.")

def hisdivide3():
    number = int(input("Enter the no. :"))
    counter = 0
    while number > 10 and number % 3 == 0:
        print(f'can divide {number} by three')
        number = number / 3
        counter += 1
        print("Number of times a given number can be divided by 3 before it is less than or equal to 10 = ", counter)

mydivide3()