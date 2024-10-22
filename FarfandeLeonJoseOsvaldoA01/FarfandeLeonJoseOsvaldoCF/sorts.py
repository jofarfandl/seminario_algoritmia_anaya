import math

def sort_by_area(circles): #Bubble sort
    for i in range(len(circles)-1): 
        for j in range(0, len(circles)-i-1): 
            if circles[j][3] > circles[j+1][3] : 
                circles[j], circles[j+1] = circles[j+1], circles[j] 
    areas = list(reversed([ (circles[i][0],round((math.pi*(circles[i][3]**2)),2)) for i in range(len(circles)) ]))
    areas = [ str(f"{areas[i][0]}    Area = {areas[i][1]}") for i in range(len(circles))]
    areas = "\n".join(areas)
    return areas

def sort_by_x(circles):#Selection sort
    for i in range(len(circles)): 
        min_idx = i 
        for j in range(i+1, len(circles)): 
            if circles[min_idx][1] > circles[j][1]:
                min_idx = j      
        circles[i], circles[min_idx] = circles[min_idx], circles[i] 
    x = [ (circles[i][0],circles[i][1]) for i in range(len(circles)) ]
    x = [ str(f"{x[i][0]}    Eje X = {x[i][1]}") for i in range(len(x))]
    x = "\n".join(x)
    return x

def sort_by_y(circles):#Insertion sort
    for i in range(1, len(circles)):
        for j in range(i - 1, -1, -1):
            if(circles[j][2] > circles[j + 1][2]):
                circles[j], circles[j + 1] = circles[j + 1], circles[j]
    y = [ (circles[i][0],circles[i][2]) for i in range(len(circles)) ]
    y = [ str(f"{y[i][0]}    Eje Y = {y[i][1]}") for i in range(len(y))]
    y = "\n".join(y)
    return y
