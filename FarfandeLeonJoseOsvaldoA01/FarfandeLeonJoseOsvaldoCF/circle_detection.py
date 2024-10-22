from cv2 import cv2
import numpy as np
from tkinter import Tk,Label,messagebox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import sorts

circles_list = []   

def no_file():#funcion para verificar si existe imagen
    messagebox.showwarning(
        title="No file",
        message="No se ha seleccionado ningún archivo"
    )

def find_circles(filename,dp,minDist,param1,param2,minRadius,maxRadius):
    if filename == "":
        no_file()
        return
    global circles_list
    circles_list.clear()
    og = mpimg.imread(filename)
    img = cv2.imread(filename,0)
    img = cv2.medianBlur(img,5)
    g_img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp,minDist,param1=param1,param2=param2,minRadius=minRadius,maxRadius=maxRadius)
    if circles is None:
        messagebox.showwarning(
            title="Fallo",
            message="No existe ningun circulo"
        )
        return
    circles = np.round(circles[0, :]).astype("int")
    i=1
    for (x, y, r) in circles:
        cv2.circle(g_img, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(g_img, (x - 3, y - 3), (x + 3, y + 3), (0, 0, 255), -1)
        cv2.putText(g_img,f"circulo_{i}",(x-30,y-r-10),cv2.FONT_HERSHEY_SIMPLEX,1,(102,17,0),2)
        circles_list.append((f"Circulo {i}",x,y,r))
        i+=1

    f = plt.figure(num = "Circulos encontrados")
    plt.imshow(cv2.cvtColor(g_img, cv2.COLOR_BGR2RGB))
    plt.show(block=False)
    show_sorts()

def show_sorts():
    root2 = Tk()
    root2.title("Ordenamientos")
    root2.resizable(0, 0)
    root2.geometry("+30+450")

    Label(
        root2,
        text = "Area",
        pady = 5,
        padx = 2,
        justify = 'center'
    ).grid(row = 0, column = 0)

    Label(
        root2,
        text = "Eje X",
        pady = 5,
        padx = 2,
        justify = 'center'
    ).grid(row = 0, column = 1)

    Label(
        root2,
        text = "Eje Y",
        pady = 5,
        padx = 2,
        justify = 'center'
    ).grid(row = 0, column = 2)

    Label(
        root2,
        text = sorts.sort_by_area(circles_list),
        pady = 5,
        padx = 15,
        justify = 'left'
    ).grid(row = 1, column = 0)

    Label(
        root2,
        text = sorts.sort_by_x(circles_list),
        pady = 5,
        padx = 15,
        justify = 'left'
    ).grid(row = 1, column = 1)

    Label(
        root2,
        text = sorts.sort_by_y(circles_list),
        pady = 5,
        padx = 15,
        justify = 'left'
    ).grid(row = 1, column = 2)

    root2.mainloop()

