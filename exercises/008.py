# Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once.
# It does not matter what you leave beyond the returned k

# My code considering nums are moved instead of being deleted
def removeDuplicates(nums):
    setnums = set(nums)
    nums2 = []
    for each in setnums:
        nums.remove(each)
        nums2.append(each)
    nums = sorted(nums2) + sorted(nums)
    k = len(setnums)
    return k, nums

# The actual Leetcode answer (when nums must return a value consisting of unique numbers from k)
def removeDuplicates2(nums):
    setnums = set(nums)
    nums.clear()                 # removes all items in a list
    nums.extend(sorted(setnums)) # assigns the set values inside a list, and sorts them ascendingly
    k = len(nums)
    return k, nums

print(removeDuplicates2([0,0,1,1,1,2,2,3,3,4]))