email = 'markschwart34@gmail.com'
array_sample = [1,2,3,4,1]

print(email[0]) #specifix index of a string
print(email[2:]) #[start:] from a specified starting index until the end. STARTING POSITION IS PRINTED
print(email[:3]) #[:end] from the start of a string until a specified end. ENDING POSITION IS NOT PRINTED
print(email[14:20]) #[start:end] combined ^
print(email[-2:]) #same concept but specified index is negative
print(email[::2]) #[start:end:step] step prints the nth instance of a number
print(email[::-1]) #returns all characters in reverse
#Best practice to use negatives when dealing with strings with a lot of characters

#What if I have a list of emails and i want to input if that email is in the dictionary
