#Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise.
#Each letter in magazine can only be used once in ransomNote.

do = 'aab' #magazine
du = 'baa' #ransomnote

def func(magazine, ransomNote):
    ransomNote2 = ransomNote
    some = ''
    for i in magazine:
        if i in ransomNote2:
            some += i
            rindex = ransomNote.index(i)
            substring1 = ransomNote[rindex+1:]
            substring2 = ransomNote[:rindex]            
            ransomNote2 = substring1 + substring2
            print()
    if some == ransomNote:
        return True
    else:
        return False

def func2(magazine, ransomNote):
    checks = ''
    for i in ransomNote:
        if i in magazine:
            magazine = magazine.replace(i, '', 1)
            checks += 'o'
        else:
            checks += 'x'
    if len(checks) == len(ransomNote) and 'x' not in checks:
        return True

print(func2(do, du))
    
