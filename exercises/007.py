#Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
#You may assume that each input would have exactly one solution, and you may not use the same element twice.
#You can return the answer in any order.
target = 9
flag = None
nums = [2,7,11,15]

# Time complexity => O(n^2)
def func(nums, target):
    while True: 
        for a_ind, a in enumerate(nums):
            for b_ind, b in enumerate(nums):
                ans = a + b
                print(f"Answer of {a}+{b} is {ans}")
                if a_ind != b_ind and ans == target:
                    print(a_ind, b_ind)
                    flag = True
                    break
            if flag:
                break
        if flag:
            break

# Time complexity => O(n) aka the BETTER SOLUTION
def func2(nums, target):
    table = {}
    for i in range(len(nums)):
        if nums[i] not in table:
            table[target-nums[i]] = i # When adding dictionary key-value pair, always make sure that you assign data, that you want to return, as a VALUE; and,
                                      # assign data that you need to iterate with, as a KEY.
        else:
            return [i, table[nums[i]]] 

print(func2(nums,target))
    