nums = [1,2,3,4,5]
k = 25

k %= len(nums)
i = len(nums) - k
new_nums = nums[i:]
other_nums = nums[:i]
nums.clear()
nums.extend(new_nums)
nums.extend(other_nums)

print(abs(i))
print(f"Nums: {nums}")
print(f"New Nums: {new_nums}")
print(f"Other Nums: {other_nums}")