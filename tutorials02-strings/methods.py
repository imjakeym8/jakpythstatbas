#This script teaches on the use cases of different python built-in string methods

def emailcheck(): #This uses .index(), .lower() and string indexing
    while True: #helps create an infinite loop, very useful for input functions.
        try:
            email = input("Please enter your email (Type 'No' to quit): ")
            if email.lower() == 'no': # .lower() returns any string to lowercase
                print("k. bye")
                break
            else:
                asterisk = email.index('@') # .index() returns an index position of a given character; it gives a ValueError if no character is found.
                username = email[:asterisk] # returns all characters before the given index position
                domain = email[asterisk+1:] # returns all characters starting from the given index position. In this case, given value is not return since we incremented it by one.
                print(f"Username is {username} and domain used is {domain}")
                break
        except ValueError:
            print("You entered the wrong email format.")
        
def emailsplit():
    while True: 
        try:
            email = input("Please enter your email (Type 'No' to quit): ")
            if email.lower() == 'no':
                print("k. bye")
                break
            else:
                email.index('@') 
                final = email.split('@')
                print(f"Username is {final[0]} and domain used is {final[1]}")
                break
        except ValueError:
            print("You entered the wrong email format.")

def ispresent(x, y):
    character = str(x)
    string = str(y)
    if character in string:
        print(f"true. {character} is in {string}")
    else:
        print(f"false. {character} is not in {string}")

def checkarray():
    nums = [3,3,7,7,10,10,11]
    for i in range(len(nums)-1):
        if nums[i] != nums[i+1] and nums[i] != nums[i-1]:
            print(nums[i])
        else:
            continue
    #Result: 2
        
checkarray()