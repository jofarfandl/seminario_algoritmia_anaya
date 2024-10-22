from cv2 import cv2
import numpy as np
from tkinter import Tk,Label,messagebox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from bresenham import bresenham
from PIL import Image
import math

def no_file():
    messagebox.showwarning(
        title="No file",
        message="No se ha seleccionado ningún archivo"
    )

#Definicion del grafo y el algoritmo de fuerza bruta
def euclidean(a, b):
    return  math.sqrt((a[1]-b[1])**2+(a[2]-b[2])**2)

class Graph:
    #Se inicializa con la lista de los vertices
    def __init__(self,vertix_list):
        self.vertix_list = vertix_list
        self.conecctions = []
        self.yellow = []
        self.result = {
            'p1':(None, None, None),
            'p2':(None, None, None),
            'min_dist': float('inf')
        }

    #Closest pair of points con fuerza bruta
    def cpp(self):
        n = len(self.vertix_list)
        for i in range(0, n-1):
            for j in range(i+1, n): 
                dist = euclidean(self.vertix_list[i], self.vertix_list[j])
                if dist < self.result['min_dist']: 
                    self.result['p1'] = self.vertix_list[i]
                    self.result['p2'] = self.vertix_list[j]
                    self.result['min_dist'] = dist
        self.yellow.append(self.result['p1'][1::])
        self.yellow.append(self.result['p2'][1::])

    def info(self):
        return f"\nLos puntos más cercanos son {self.result['p1'][0]} y {self.result['p2'][0]}.\n\nV.{self.result['p1'][0]} {self.result['p1'][1::]} --- V.{self.result['p2'][0]} {self.result['p2'][1::]}\n\nDistancia entre los 2 puntos es: {self.result['min_dist']:.2f}"

    #Funcion que retorna la información de los vertices conectados en formato para la label
    def v(self):
        x = [ f"({i[0]},{i[1]})" for i in self.conecctions]
        x = "\n".join(x)
        return f"Vertices conectados\n{x}\n"

#Funcion que dibuja los grafos
def draw_graphs(filename,dp,minDist,param1,param2,minRadius,maxRadius):
    if filename == "":
        no_file()
        return
    image = Image.open(filename)
    image = image.convert('RGB')
    obstacle_coords = {}

    #Diccionario con todas las coordenadas de los obstaculos
    for y in range(image.height):
        for x in range(image.width):
            r,g,b = image.getpixel((x, y))
            if r == g and g == b:
                pass
            else:
                obstacle_coords[f'{x},{y}'] = (x,y)

    #Configuracion de la ventana
    circles_list = []
    og = mpimg.imread(filename)
    v = cv2.cvtColor(mpimg.imread(filename),cv2.COLOR_RGB2BGR)
    img = cv2.imread(filename,0)
    img = cv2.medianBlur(img,5)

    #Deteccion de circulos (Vertices)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp,minDist,param1=param1,param2=param2,minRadius=minRadius,maxRadius=maxRadius)
    if circles is None:
        messagebox.showwarning(
            title="No circles",
            message="No se ha encontrado ningún vertice"
        )
        return
    circles = np.round(circles[0, :]).astype("int")
    i=1

    for (x, y, r) in circles:
        cv2.circle(v, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(v, (x - 3, y - 3), (x + 3, y + 3), (0, 0, 255), -1)
        cv2.putText(v,f"V.{i}",(x-30,y-r-10),cv2.FONT_HERSHEY_SIMPLEX,.75,(0,0,0),2)

        circles_list.append((i,x,y,r))
        i+=1

    #Creación del grafo con todos los vertices y su coordenada
    global graph
    graph = Graph([ (i[0],i[1],i[2]) for i in circles_list ])

    #Se busca si la línea cruza por algún obstaculo con bresenham y el diccionario con los obstaculos
    # y despues se dibuja la línea
    for (n,x,y,r) in circles_list:
        for vertice in circles_list:
            if n == vertice[0]:
                pass
            else:
                for (x1,y1) in list(bresenham(x,y,vertice[1],vertice[2])):
                    if f"{x1},{y1}" in obstacle_coords:
                        found = False
                        break
                    else:
                        found = True
                lig = (n,vertice[0])
                r_lig = (lig[::-1])
                if found == True and (lig not in graph.conecctions and r_lig not in graph.conecctions):
                    cv2.line(v,(x,y),(vertice[1],vertice[2]),(255,0,0),2)
                    graph.conecctions.append(lig)

    #Se resaltan los puntos más cercanos
    graph.cpp()
    cv2.line(v,graph.yellow[0],graph.yellow[1],(0,0,255),3)

    #Se muestra la ventana con la imagen original y la otra con la unión de los vertices
    f = plt.figure(num = "Grafo generado")
    
    #f.add_subplot()
    plt.imshow(cv2.cvtColor(v, cv2.COLOR_RGB2BGR))
    plt.show(block=False)
    show_graph_info()

def show_graph_info():
    root2 = Tk()
    root2.title("Datos del grafo")
    root2.resizable(0, 0)
    root2.geometry("+30+450")

    Label(
        root2,
        text = f"{graph.info()}\nResaltado en color rojo",
        pady = 5,
        padx = 10,
        justify = 'center'
    ).grid(row = 0, column = 0)

    Label(
        root2,
        text = graph.v(),
        pady = 5,
        padx = 2,
        justify = 'center'
    ).grid(row = 1, column = 0)

    root2.mainloop()
