import scipy
import numpy as np
import math as m

def f2(x1,x2):
    t1 =  0.7 * m.exp(-((10*x1-2)**2+(9*x2-2)**2)/4)
    t2 = 0.65*m.exp(-(((9*x1+1)**2)/9) -((10*x2+1)**2)/2)
    t3 = 0.5 * m.exp(-((9*x1-6)**2)/4 - ((9*x2-3)**2)/4) 
    t4 = - 0.01 * m.exp(-((9*x1-7)**2)/4 - ((9*x2-3)**2)/4)
    return t1 + t2 + t3 + t4

# ---------------- GENERADORES DE PUNTOS EQUIESPACIADOS Y NO EQUIESPACIADOS --------------   

def generar_puntos_equiespaciados(lim_inferior, lim_superior, cantidad_de_puntos, f):
    points_x1_x2 = np.linspace(lim_inferior, lim_superior, cantidad_de_puntos)
    x1_grid, x2_grid = np.meshgrid(points_x1_x2, points_x1_x2) 
    combinations = np.column_stack((x1_grid.flatten(), x2_grid.flatten())) #Se ve de la forma: {[x11,x21][x11,x22][...]...}
    dataset = {}
    for combination in combinations:
        dataset[combination] = f(combination[0], combination[1])      
    return dataset


#CHEBYSHEV

def generar_puntos_chebyshev(lim_inferior, lim_superior, cantidad_de_puntos, f):
    points = np.zeros(cantidad_de_puntos)
    for i in range(cantidad_de_puntos):
        points[i] = (lim_inferior + lim_superior) / 2 + ((lim_superior - lim_inferior) / 2) * np.cos(((2 * i + 1) * np.pi) / (2 * cantidad_de_puntos))
    
    x1_grid, x2_grid = np.meshgrid(points, points) 
    combinations = np.column_stack((x1_grid.flatten(), x2_grid.flatten()))

    dataset = {}
    for combination in combinations:
        dataset[combination] = f(combination[0], combination[1])
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
#rescale: probarlo con True y False, ver en qué caso el error se me hace menor!

#Interpolación con nearest neighbor.
def NearestNeighbor(x, y, x_eval):
    scipy.interpolate.griddata(x, y, x_eval, method='nearest', fill_value=nan, rescale=False)
    return

#Interpolación con splines lineales.
def Spline_1(x,y, x_eval):
    scipy.interpolate.griddata(x, y, x_eval, method='cubic', fill_value=nan, rescale=False)
    return

#Interpolación con splines cúbicos.
def Spline_3(x,y, x_eval):
    scipy.interpolate.griddata(x, y, x_eval, method='linear', fill_value=nan, rescale=False)
    return



#-----------------------------------------------------------


    

def main():
    # Array con diferentes cantidades de puntos
    different_quantity_equiesp_points = [15, 30, 50]
    INFO_DICC_FUNCTION = {} 

    #Array con puntos (100) en los que vamos a testear las interpolaciones para obtener los errores:
    testing_points = generar_puntos_equiespaciados(-4,4, 1000, f1)
    x_testing = list(testing_points.keys()) #[(x11,x21), (x11, x22), ...]
    x_testing = np.vstack(x_testing)
    y_testing = list(testing_points.values())
    y_testing = np.vstack(y_testing)
    
    
    INFO_DICC_NN = {}
    INFO_DICC_SPL_1 = {}
    INFO_DICC_SPL_3 = {}
    
    for i in range(3):
        # Creamos un subplot para el gráfico actual 
        fig = plt.figure(figsize=(16, 6))
        
        # Generar puntos equiespaciados y de Chebyshev
        dicc_equiesp = generar_puntos_equiespaciados(-4, 4, different_quantity_equiesp_points[i], f2)
        
        dicc_chebyshev = generar_puntos_chebyshev(-4, 4, different_quantity_equiesp_points[i], f2)
        

        # Puntos conocidos por ambas funciones
        x_equiesp = list(dicc_equiesp.keys()) # lista de numpy arrays de 1x2
        x_equiesp = np.vstack(x_equiesp)
        y_equiesp = list(dicc_equiesp.values())
        y_equiesp = np.vstack(y_equiesp)

        
        x_chebyshev = list(dicc_chebyshev.keys())
        x_chebyshev = np.vstack(x_chebyshev)
        y_chebyshev = list(dicc_chebyshev.values())
        y_chebyshev = np.vstack(y_chebyshev)
        

    # Nearest Neighbor
        # Calculamos interpolación por el método del Nearest Neighbor
        NN_testing_y = NearestNeighbor(x_equiesp, y_equiesp, x_testing) 
       # Calculamos el error de aproximar con Lagrange
        error_rel_NN = error_relativo(NN_testing_y, y_testing)

    # Spline Cubic
        # Calculamos el polinomio con SplineCubic
        CubicSpl_testing_y = Spline_Cubic(x_equiesp, y_equiesp, x_testing)
    # Calculamos el error de aproximar con Lagrange
        error_rel_cub = error_relativo(CubicSpl_testing_y, y_testing)

    # Spline Cubic
        # Calculamos el polinomio con SplineCubic
        LinealSpl_testing_y = Spline_Lineal(x_equiesp, y_equiesp, x_testing)
    # Calculamos el error de aproximar con Lagrange
        error_rel_lin = error_relativo(LinealSpl_testing_y, y_testing)

    
    # Chebyshev
        # Calculamos el polinomio de Chebyshev
        Cheb_function = Chebyshev(x_chebyshev, y_chebyshev)
        chebyshev_testing_y = Cheb_function(x_testing)
       # Calculamos el error de aproximar con Lagrange
        error_rel_cheb = error_relativo(chebyshev_testing_y, y_testing)
    

    # Graficamos los errores de aproximar con el método del Nearest Neighbor
        plt.subplot(4, 1, 1)
        plt.plot(x_testing, error_rel_lag, 'b-', label='Error Relativo')
        plt.legend()
        plt.title(f'Gráfico de error relativo al aproximar con el método del Nearest Neighbor con {different_quantity_equiesp_points[i]} puntos')

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