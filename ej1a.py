import scipy
import numpy as np
import math as m

def f1(x):
    return (0.3**np.abs(x))*m.sin(4*x) - m.tanh(2*x) + 2
    
def generar_puntos_equiespaciados(lim_inferior, lim_superior, cantidad_de_puntos, f):
    points = np.linspace(lim_inferior, lim_superior, cantidad_de_puntos)
    dataset = {}
    for x in points:
        dataset[x] = f(x)
    return dataset
    
#EA Y ER (errores): con cada función 

def error_absoluto(real, aprox):
    ea_arr = []
    for i in range(len(real)):
        ea = np.abs(real - aprox)
        ea_arr.append(ea)
    return ea_arr
    
def error_relativo(real, aprox):
    ea = error_absoluto(real,aprox)
    er_arr = []
    for i in range(len(ea)):
        er = ea[i] / np.abs(real)
        er_arr.append(er)
    return er_arr
    

#Función de nodos de chebyshev...

#Interpolación en Lagrange
def Lagrange(x, y):
    
    return

#Interpolación con splines lineales
def Spline_1(x,y):
    
    return

#Interpolación con splines cúbicos.
def Spline_3(x,y):
    
    return


def main():
    #Array con diferentes cantidades de puntos
    different_quantity_equiesp_points = [15, 30, 50]
    
    INFO_DICC_FUNCTION = {}
    #Luego del test:
    INFO_DICC_LAGR = {}
    INFO_DICC_SPL_1 = {}
    INFO_DICC_SPL_3 = {}
    
    for i in range(3):
        dicc = generar_puntos_equiespaciados(-4,4, different_quantity_equiesp_points[i], f1)
        INFO_DICC_FUNCTION[different_quantity_equiesp_points[i]] = dicc
        
        Lagr_function = Lagrange(dicc.keys, dicc.values)
        Spline_1_function = Spline_1(dicc.keys, dicc.values)
        Spline_3_function = Spline_3(dicc.keys, dicc.values)
        
        #Graficamos cada función. (pendiente)
        
        
        
        #Calculamos los errores absolutos y relativos de los diferentes métodos de interpolación:

        #Array con puntos (100) en los que vamos a testear las interpolaciones para obtener los errores:
        testing_points = generar_puntos_equiespaciados(-4,4, 100)
    
    
    
    

if __name__ == '__main__':
    main()