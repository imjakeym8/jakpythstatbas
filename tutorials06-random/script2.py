import random

nums = set()
i = 0

while i < 8:
    x = random.randint(979, 1000)
    if x not in nums:
        nums.add(x)
        i += 1

finnums = list(sorted(nums))
print(finnums)
