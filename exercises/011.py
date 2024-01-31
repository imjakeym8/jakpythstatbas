# Given a string s, find the length of the longest substring without repeating characters.
# Note: A substring is a contiguous non-empty sequence of characters within a string.

s = "abcadbcbb"

subs = ''

for i in range(len(s)): 
    for char in s[i:]:
        if char in subs:
            break
        subs += char
    subs_copy = subs
    subs = ''

print(subs)
    

# for i in range(len(s)): 
#         if s[i] in subs:
#             break
#         subs += s[i]

# print(subs)

