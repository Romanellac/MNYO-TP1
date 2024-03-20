import scipy
import numpy as np
import math as m
from scipy.interpolate import lagrange, CubicSpline, interp1d
import matplotlib.pyplot as plt

def f1(x):
    return (0.3**np.abs(x))*m.sin(4*x) - m.tanh(2*x) + 2


# ---------------- GENERADORES DE PUNTOS EQUIESPACIADOS Y NO EQUIESPACIADOS --------------   
def generar_puntos_equiespaciados(lim_inferior, lim_superior, cantidad_de_puntos, f):
    points = np.linspace(lim_inferior, lim_superior, cantidad_de_puntos)
    dataset = {}
    for x in points:
        dataset[x] = f(x)
    return dataset

def generar_puntos_chebyshev(lim_inferior, lim_superior, cantidad_de_puntos, f):
    points = np.zeros(cantidad_de_puntos)
    for i in range(cantidad_de_puntos):
        points[i] = (lim_inferior + lim_superior) / 2 + ((lim_superior - lim_inferior) / 2) * np.cos(((2 * i + 1) * np.pi) / (2 * cantidad_de_puntos))
    
    dataset = {}
    for x in points:
        dataset[x] = f(x)
    return dataset


# ---------------- ERRORES --------------   
#EA Y ER (errores): con cada función 
def error_absoluto(real, aprox):
    ea_arr = []
    for i in range(len(real)):
        ea = np.abs(real[i] - aprox[i])
        ea_arr.append(ea)
    return ea_arr
    
def error_relativo(real, aprox):
    er_arr = []
    for i in range(len(real)):
        if real[i] != 0:
            er = np.abs((real[i] - aprox[i]) / real[i])
        else:
            er = np.abs(aprox[i])
        er_arr.append(er)
    return er_arr




# --------------------- INTERPOLACIONES  -----------------------   

#Interpolación de nodos de chebyshev...
def Chebyshev(x, y):
    return lagrange(x, y)

#Interpolación en Lagrange
def Lagrange(x, y):
    return lagrange(x, y)

#Interpolación con splines lineales
def Spline_Lineal(x,y):
    return interp1d(x, y, kind='linear', fill_value='extrapolate')

#Interpolación con splines cúbicos.
def Spline_Cubic(x,y):
    return CubicSpline(x, y)






def main():

    # Array con diferentes cantidades de puntos
    different_quantity_equiesp_points = [5, 9, 16]
    INFO_DICC_FUNCTION = {}

    #Array con puntos (100) en los que vamos a testear las interpolaciones para obtener los errores:
    testing_points = generar_puntos_equiespaciados(-4,4, 1000, f1)
    x_testing = list(testing_points.keys())
    y_testing = list(testing_points.values())
    
    for i in range(3):
        # Creamos un subplot para el gráfico actual
        fig = plt.figure(figsize=(16, 6))
        
        # Generar puntos equiespaciados y de Chebyshev
        dicc_equiesp = generar_puntos_equiespaciados(-4, 4, different_quantity_equiesp_points[i], f1)
        dicc_chebyshev = generar_puntos_chebyshev(-4, 4, different_quantity_equiesp_points[i], f1)
        
        # Puntos conocidos por ambas funciones
        x_equiesp = list(dicc_equiesp.keys())
        y_equiesp = list(dicc_equiesp.values())
        x_chebyshev = list(dicc_chebyshev.keys())
        y_chebyshev = list(dicc_chebyshev.values())

    # LAGRANGE
        # Calculamos el polinomio de Lagrange
        Lagr_function = Lagrange(x_equiesp, y_equiesp)
        lagrange_testing_y = Lagr_function(x_testing)
       # Calculamos el error de aproximar con Lagrange
        error_rel_lag = error_relativo(lagrange_testing_y, y_testing)

    # Spline Cubic
        # Calculamos el polinomio con SplineCubic
        CubicSpl_function = Spline_Cubic(x_equiesp, y_equiesp)
        CubicSpl_testing_y = CubicSpl_function(x_testing)
       # Calculamos el error de aproximar con Lagrange
        error_rel_cub = error_relativo(CubicSpl_testing_y, y_testing)

    # Spline Cubic
        # Calculamos el polinomio con SplineCubic
        LinealSpl_function = Spline_Lineal(x_equiesp, y_equiesp)
        LinealSpl_testing_y = LinealSpl_function(x_testing)
       # Calculamos el error de aproximar con Lagrange
        error_rel_lin = error_relativo(LinealSpl_testing_y, y_testing)
    
    # Chebyshev
        # Calculamos el polinomio de Chebyshev
        Cheb_function = Chebyshev(x_chebyshev, y_chebyshev)
        chebyshev_testing_y = Cheb_function(x_testing)
       # Calculamos el error de aproximar con Lagrange
        error_rel_cheb = error_relativo(chebyshev_testing_y, y_testing)


    # Graficamos los errores de aproximar con Lagrange
        plt.subplot(4, 1, 1)
        plt.plot(x_testing, error_rel_lag, 'b-', label='Error Relativo')
        plt.legend()
        plt.title(f'Gráfico de error relativo al aproximar con Lagrange con {different_quantity_equiesp_points[i]} puntos')

    # Graficamos los errores de aproximar con Spline Cubic
        plt.subplot(4, 1, 2)
        plt.plot(x_testing, error_rel_cub, 'b-', label='Error Relativo')
        plt.legend()
        plt.title(f'Gráfico de error relativo al aproximar con Cubic Splines con {different_quantity_equiesp_points[i]} puntos')

    # Graficamos los errores de aproximar con Spline Lineal
        plt.subplot(4, 1, 3)
        plt.plot(x_testing, error_rel_lin, 'b-', label='Error Relativo')
        plt.legend()
        plt.title(f'Gráfico de error relativo al aproximar con Lineal Splines con {different_quantity_equiesp_points[i]} puntos')

    # Graficamos los errores de aproximar con Chebyshev
        plt.subplot(4, 1, 4)
        plt.plot(x_testing, error_rel_cheb, 'b-', label='Error Relativo')
        plt.legend()
        plt.title(f'Gráfico de error relativo al aproximar con Chebyshev con {different_quantity_equiesp_points[i]} puntos')
        
        plt.tight_layout()
        plt.show()

    

if __name__ == '__main__':
    main()