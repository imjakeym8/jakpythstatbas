# You are given an array coordinates, coordinates[i] = [x, y], where [x, y] represents the coordinate of a point. 
# Check if these points make a straight line in the XY plane.
'''
Line 16 was originally from the slope equation: m = (y1-y0) / (x1-x0) 
The goal is to check if the slope would be equal in order to return True: (y1-y0) / (x1-x0) = (y-y0) / (x-x0)
So, we trasponsed each expression on each side to multiplication, ESPECIALLY since dividing by 0 will result to ZeroDivisionError, while still ACHIEVING THE SAME GOAL.
'''
coordinates = [[1,2],[2,4],[3,6],[4,8],[5,10]]

def checkStraightLine(coordinates: list[list[int]]) -> bool:
    x0, y0 = coordinates[0]
    x1, y1 = coordinates[1]
    flag = True
    for i in range(2, len(coordinates)):
        x, y = coordinates[i]
        if (x - x0) * (y1 - y0) !=  (x1 - x0) * (y - y0): 
            flag = False                                  
            break                                         
    return flag                                           

print(checkStraightLine(coordinates=coordinates))











