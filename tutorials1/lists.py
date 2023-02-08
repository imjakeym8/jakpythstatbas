#1st problem
def count_characters(string_list):
    count = 0
    for each_item in string_list:
        count += len(each_item)
    return count

countries = ["India", "Germany", "Japan"]
print("Number of characters:", count_characters(countries))


