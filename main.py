import numpy as np
import matplotlib.pyplot as graf

def metodo_simplex(variables,restricciones): 
    encabezados = []                        #creamos los respectivos encabezados en x para que tengan formato 
    for k in range(1, variables + 1):
        encabezados.append(f"x{k}")
    for p in range(1, restricciones + 1):
        encabezados.append(f"s{p}")
    encabezados.append("Solución:")

    laterales = ["Z"]                      

    for i in range(1, restricciones + 1):
        laterales.append(f"s{i}")


    tabla = [] #inicializamos una lista en donde se guardaran los datos_usuario del usuario

    print("\n-- Función Objetivo (ingresa los coeficientes de la función a maximizar) --")

    # FILA DE LA FUNCIÓN OBJETIVO (Z)
    print(f"\nFila '{laterales[0]}':") #pedimos el coeficiente de la func objetivo
    fila_z = [] 
    
    for j in range(len(encabezados)):
        if j < variables:
            # BLOQUE DE ROBUSTEZ: Coeficientes de la función objetivo (Z)
            while True:
                try:
                    valor = float(input(f"  {encabezados[j]}    = "))
                    fila_z.append(-valor) # agregamos los coeficientes con el valor negativo
                    break # Sale del bucle while si la entrada es válida
                except ValueError:
                    print("Entrada no válida, ingresa un número.")
        else:
            # despues de las variables, las s de holgura y la solución son 0
            fila_z.append(0.0)
    tabla.append(fila_z)


    # FILAS DE LAS RESTRICCIONES (s1, s2 ....)
    for i in range(1, len(laterales)):  # i recorre las filas de s empezando de la 2 o indice 1
        fila = []
        # La variable de holgura que corresponde a esta fila es s(i-1)
        diagonal = variables + (i - 1) 
        
        print(f"\nFila '{laterales[i]}':")
        for j in range(len(encabezados)):
            
            if j < variables:  #se agregan los coeficientes de las restricciones
                # BLOQUE DE ROBUSTEZ -> Coeficientes de las restricciones (a1, a2, ...)
                while True:
                    try:
                        valor = float(input(f"  {encabezados[j]} = "))
                        fila.append(valor)
                        break # Sale del bucle while si la entrada es válida
                    except ValueError:
                        print("Entrada no válida, ingresa un número.")
                    
            elif j == len(encabezados) - 1:  # columna de solución
                # BLOQUE DE ROBUSTEZ -> Columna de Solución (b)
                while True:
                    try:
                        valor = float(input("  Solución = "))
                        fila.append(valor)
                        break # Sale del bucle while si la entrada es válida
                    except ValueError:
                        print("Entrada no válida, ingresa un número.")
                
            elif j >= variables and j < len(encabezados) - 1: # columnas de holgura (s1, s2, ...)
                if j == diagonal:  # Si la columna actual j es la columna de su propia variable de holgura
                    fila.append(1.0)      # Coloca un 1 ya que esa variable de holgura le pertence a esa restriccion
                else:                     
                    fila.append(0.0)      # Coloca un 0 porque no tiene valor
        tabla.append(fila)  #se agrega renglón por renglón

        

    print("\n--- TABLA INICIAL ---\n")
    print("       ", end="")            #imprimimos los encabezados de la tabla inicial
    for e in encabezados:
        print(f"{e:^10}", end="")
    print()


    for i in range(len(laterales)):
        print(f"{laterales[i]:<5} |", end=" ")
        for valor in tabla[i]:
            # Usamos .2f para una mejor visualización de los decimales
            print(f"{valor:^10.2f}", end="") 
        print()


    iteracion = 1
    num_filas = len(tabla)
    num_cols = len(tabla[0])

    while True:
        print(f"\n******************** ITERACIÓN {iteracion} ********************")
        
        #encontrar la variable pivote
        col_pivote = -1
        minimo_valor = 0
        fila_z = tabla[0]
        
        for j in range(num_cols - 1): # buscar entre cada elemento del renglón excluyendo la solución
            if fila_z[j] < minimo_valor:
                minimo_valor = fila_z[j]
                col_pivote = j
                
        #condición de paro ya que si todas las variable baśicas son positivas, hemos llegado a la solución optima
        if col_pivote == -1:
            print("\n¡Óptimo alcanzado! Todos los valores de la fila Z son positivos.")
            break   
        
        print(f"Columna Pivote (Entrante): {encabezados[col_pivote]}")
        
        #encontrar el renglón pivote
        renglon_pivote = -1
        min_division = float('inf')
        
        for i in range(1, num_filas): # Comienza en la fila 1 (excluye la fila Z)
            temp_renglon = tabla[i][col_pivote]
            val_solucion = tabla[i][-1]
            
            # Solo considera divisores positivos para el cociente
            if temp_renglon > 0:
                division = val_solucion / temp_renglon
                if division < min_division:
                    min_division = division
                    renglon_pivote = i
                            
        print(f"Fila Pivote (Saliente): {laterales[renglon_pivote]}")
        
        #cambio de encabezados por las nuevas variables
        laterales[renglon_pivote] = encabezados[col_pivote]
        
        #obtenemos el cruze de columna pivote y renglon pivote 
        elemento_pivote = tabla[renglon_pivote][col_pivote]
        
        for j in range(num_cols):
            #dividimos cada valor de renglón pivote sobre el elemento pivote
            tabla[renglon_pivote][j] /= elemento_pivote

        for i in range(num_filas):
            #Ignoramos el renglón pivote, ya que tiene el 1 en la columna pivote.
            if i != renglon_pivote:
                
                #obtenemos el valor que queremos convertir en 0
                valor_a_eliminar = tabla[i][col_pivote]
                
                # aplicamos la operación entre todos los elementos del renglón actual
                for j in range(num_cols):
                    tabla[i][j] -= valor_a_eliminar * tabla[renglon_pivote][j]

        
        # Mostrar tabla después del pivoteo
        print("       ", end="")
        for e in encabezados:
            print(f"{e:^10}", end="")
        print()
        for i in range(len(laterales)):
            print(f"{laterales[i]:<5} |", end=" ")
            for valor in tabla[i]:
                print(f"{valor:^10.4f}", end="") 
            print()

        iteracion += 1

    #mostramos la solución final
    print("\n******************** SOLUCIÓN FINAL ********************")

    # El valor óptimo de Z está en la última columna
    zMax_optimo = tabla[0][-1]
    print(f"El valor óptimo de la Función Objetivo Z es: {zMax_optimo:.2f}")

    print("\nValores de las Variables:")

    for i in range(1, len(laterales)):
        var_nombre = laterales[i]
        
        # Si la variable es una x (básica), su valor es el de la columna "Solución" en esa fila
        if var_nombre.startswith('x'):
            valor = tabla[i][-1]
            print(f"  {var_nombre} = {valor:.2f}")
            continue
        print(f"{var_nombre} = 0 ")

    # Las variables que no están en la lista 'laterales' (no básicas) tienen valor 0.

def metodo_grafico(num_restricciones):
    
    #ingresar los coeficientes de la func objetivo
    print("\n--- Coeficientes de la Función Objetivo (Z) ---")
    while True:
        try:
            # Pedimos los coeficientes de Z (variables c1 y c2)
            c1 = float(input("Coeficiente de X1 en Z: "))
            c2 = float(input("Coeficiente de X2 en Z: "))
            break # Salimos del bucle si ambas entradas son válidas
        except ValueError:
            print("Entrada no válida, ingresa un número.")

    #ingresamos las restricciones    
    datos_restr = []
    max_num_x = 0  # Variable para rastrear el mayor coeficiente en X1 entre las restricciones
    for i in range(num_restricciones):
        print(f"\n--- Coeficientes de la Restricción {i+1} ---")
        while True:
            try:
                # Pedimos los coeficientes de la restricción
                a_i = float(input("Coeficiente X1: "))
                b_i = float(input("Coeficiente X2: "))
                r_i = float(input("Lado derecho <= : "))
                
                datos_restr.append((a_i, b_i, r_i))
                max_temp = r_i / a_i if a_i != 0 else 0
                break # Salimos del bucle si las tres entradas son válidas
            except ValueError:
                print("Entrada no válida en la restricción, ingresa números.")
        max_num_x = max(max_num_x, max_temp)  # Actualizamos el mayor coeficiente en X1 para ver de mejor manera el gráfico
    
    # Definimos el rango de valores para X1
    eje_x1 = np.linspace(0, max_num_x, 200)
    
    # Inicializamos X2_max_región con un valor muy alto
    x2_max_region = np.full_like(eje_x1, 1000000) 
    
    # Creamos la figura
    graf.figure(figsize=(9,7))

    for i, (a_i, b_i, r_i) in enumerate(datos_restr):
        nombre_restriccion = f'R{i+1}'
        
        # Caso 1: Restricción vertical (X2 no existe, a2 = 0)
        if b_i == 0:
            limite_x1 = r_i / a_i
            graf.axvline(limite_x1, linestyle='--', color='darkblue', label=nombre_restriccion)
            x2_max_region[eje_x1 > limite_x1] = 0 # La región factible termina aquí
        
        # Caso 2: Restricción normal (X2 existe, a2 != 0)
        else:
            # Despejamos X2: X2 = (b - a1*X1) / a2
            eje_x2 = (r_i - a_i * eje_x1) / b_i
            
            graf.plot(eje_x1, eje_x2, label=nombre_restriccion, color=graf.cm.viridis(i/num_restricciones))
            
            # Actualizamos el límite de la región factible (tomamos el mínimo)
            x2_max_region = np.minimum(x2_max_region, eje_x2)

    # Aseguramos que X2_max_region nunca sea negativo (debido a la restricción de no negatividad)
    x2_final_region = np.maximum(x2_max_region, 0)
    
    # Rellenamos la Región Factible
    graf.fill_between(eje_x1, 0, x2_final_region, 
                     where=x2_final_region > 0, 
                     color='gold', alpha=0.5, 
                     label='Región Factible')

    #calculamos puntos extremos y solucuión óptima

    puntos_extremos = {(0, 0)} # Punto de origen
    
    # Buscamos intersecciones entre restricciones
    num_restr = len(datos_restr)
    for i in range(num_restr):
        for j in range(i + 1, num_restr):
            
            # Extraer coeficientes para formar la matriz del sistema de ecuaciones
            a1_i, a2_i, b_i = datos_restr[i]
            a1_j, a2_j, b_j = datos_restr[j]
            
            matriz_A = np.array([[a1_i, a2_i], [a1_j, a2_j]])
            vector_B = np.array([b_i, b_j])
            
            # Calculamos el determinante
            determinante = np.linalg.det(matriz_A)
            
            # Si el determinante es diferente de 0, hay solución única
            if determinante != 0:
                solucion = np.linalg.solve(matriz_A, vector_B)
                coord_x1, coord_x2 = solucion[0], solucion[1]
                
                # Verificamos que el punto esté en la región factible (X1>=0, X2>=0 y cumple todas las restricciones)
                es_factible = coord_x1 >= 0 and coord_x2 >= 0 and \
                              all(a_i*coord_x1 + b_i*coord_x2 <= r_i + 1e-9 for a_i, b_i, r_i in datos_restr)
                
                if es_factible:
                    # Redondeamos antes de agregar
                    punto_redondeado = (round(coord_x1, 4), round(coord_x2, 4))
                    puntos_extremos.add(punto_redondeado)
                    
    # Buscamos intersecciones con los ejes (X1 y X2)
    for a_i, b_i, r_i in datos_restr:
        # Intersección con el eje X1 (X2=0)
        if a_i != 0 and r_i / a_i >= 0: 
            punto_eje_x1 = (r_i / a_i, 0)
            puntos_extremos.add(punto_eje_x1)
            
        # Intersección con el eje X2 (X1=0)
        if b_i != 0 and r_i / b_i >= 0: 
            punto_eje_x2 = (0, r_i / b_i)
            puntos_extremos.add(punto_eje_x2)

    # Evaluación de la Función Objetivo (Z)
    max_z_valor, punto_optimo = -1e9, None
    for coord_x1, coord_x2 in puntos_extremos:
        
        # Recalculamos la factibilidad para asegurar
        if all(a_i*coord_x1 + b_i*coord_x2 <= r_i + 1e-9 for a_i, b_i, r_i in datos_restr):
            
            # Calculamos el valor de Z
            valor_z = c1 * coord_x1 + c2 * coord_x2
            
            # Ploteamos el punto extremo (color: 'black')
            graf.plot(coord_x1, coord_x2, 'ko')
            
            # Agregamos anotación
            etiqueta_punto = f"({coord_x1:.1f},{coord_x2:.1f})"
            graf.annotate(etiqueta_punto, (coord_x1, coord_x2), textcoords="offset points", xytext=(6,6))
            
            # Verificamos si es el nuevo óptimo
            if valor_z > max_z_valor: 
                max_z_valor = valor_z
                punto_optimo = (coord_x1, coord_x2)

    #resultados y graficación del punto óptimo
    
    if punto_optimo:
        #resaltamos el punto óptimo
        graf.plot(punto_optimo[0], punto_optimo[1], 'r*', markersize=18, label=f'Óptimo Z={max_z_valor:.2f}')
        print(f"\nÓptimo en X1={punto_optimo[0]:.2f}, X2={punto_optimo[1]:.2f}, Z={max_z_valor:.2f}")
    else:
        print("\nNo hay región factible ")

    # Configuración final del gráfico
    titulo_grafico = f'Método Gráfico: Max Z = {c1}X1 + {c2}X2'
    graf.title(titulo_grafico)
    graf.xlabel('X1'); 
    graf.ylabel('X2'); 
    graf.grid(True, linestyle='--'); 
    graf.legend()
    graf.ylim(bottom=0)
    graf.xlim(left=0)

    # Guardamos la imagen
    nombre_archivo = "grafico_pl.png"
    graf.savefig(nombre_archivo)
    print(f"\nGráfico guardado como '{nombre_archivo}'")
# BLOQUE DE ROBUSTEZ -> Variables y Restricciones
while True:
    try:
        print("PROGRAMA PARA SOLUCIONAR PROBLEMAS DE PROGRAMACIÓN LINEAL UTILIZANDO EL MÉTODO SIMPLEX")
        variables = int(input("¿Cuántas variables tiene tu modelo? "))
        restricciones = int(input("¿Cuántas restricciones tiene tu modelo? "))
        break
    except ValueError:
        print("Entrada no válida, ingresa un número entero.\n")

# Validar método
while True:
    metodo = input("Método por el que lo quieras resolver (Simplex -> S) o (Gráfico -> G): ").strip().upper()
    if metodo in ("S", "G"):
        break
    else:
        print("Opción no válida, ingresa solo 'S' o 'G'.\n")

if metodo == 'G' and variables == 2:
    metodo_grafico(restricciones)
elif metodo == 'G' and variables >2:
    print("No se puede resolver por método gráfico, escoge la opción Simplex")
elif metodo == 'S':
    metodo_simplex(variables,restricciones)