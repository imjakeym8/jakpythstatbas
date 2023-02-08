#2nd problem
#how do we write this using lists and for loop ???

def myorder(list):
    for each_item in list:
        print(each_item)

def list_visit(list, list2):
    for each_item in list:
        for each_item2 in list2:
            print("In", each_item + ",", "the monument to visit is", each_item2)
def visit(dict):
    for a, b in dict.items():
        print("In", a + ",", "the monument to visit is", b)

l1 = ["New York", "Orlando", "Toronto"]
l2 = ["Statue of Liberty", "Stokes", "Fort Rouille"]
#new_dict = dict(zip(l1, l2))

list_visit(l1, l2)