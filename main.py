print("PROGRAMA PARA SOLUCIONAR PROBLEMAS DE PROGRAMACIÓN LINEAL UTILIZANDO EL MÉTODO SIMPLEX")
variables = int(input("¿Cuántas variables tiene tu modelo? "))
restricciones = int(input("Cuántas restricciones tiene tu modelo? "))

encabezados = []                        #creamos los respectivos encabezados en x para que tengan formato
for k in range(1, variables + 1):
    encabezados.append(f"x{k}")
for p in range(1, restricciones + 1):
    encabezados.append(f"s{p}")
encabezados.append("Solución:")

laterales = ["Z"]                       #creamos los respectivos encabezados en y para que tengan formato
for i in range(1, restricciones + 1):
    laterales.append(f"s{i}")


tabla = [] # Usamos 'tabla' en lugar de 'tabla_inicial' para el proceso
funcion_objetivo = []

print("\n-- Función Objetivo (ingresa los coeficientes de la función a maximizar) --")

# FILA DE LA FUNCIÓN OBJETIVO (Z)
print(f"\nFila '{laterales[0]}':") #mostramos encabezados
fila_z = [] 
for j in range(len(encabezados)):
        if j < variables:
            # Pide coeficientes y los convierte a negativo para Simplex de maximización
            valor = float(input(f"  {encabezados[j]}    = "))
            fila_z.append(-valor) # ¡Coeficientes de Z en negativo!
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
            valor = float(input(f"  {encabezados[j]} = "))
            fila.append(valor)

        elif j == len(encabezados) - 1:  # columna de solución
            valor = float(input("  Solución = "))
            fila.append(valor)
            
        elif j >= variables and j < len(encabezados) - 1: # columnas de holgura (s1, s2, ...)
            if j == diagonal:  # Si la columna actual j es la columna de su propia variable de holgura
                fila.append(1.0)      # Coloca un 1 ya que esa variable de holgura le pertence a esa restriccion
            else:                     
                fila.append(0.0)      # Coloca un 0 porque no tiene valor
    tabla.append(fila)  #se agrega renglón por renglón

    

print("\n--- TABLA INICIAL ---\n")
print("       ", end="")            #imprimimos los encabezados 
for e in encabezados:
    print(f"{e:^10}", end="")
print()


for i in range(len(laterales)):
    print(f"{laterales[i]:<5} |", end=" ")
    for valor in tabla[i]:
        # Usamos .4f para una mejor visualización de los decimales
        print(f"{valor:^10.4f}", end="") 
    print()


iteracion = 1
num_filas = len(tabla)
num_cols = len(tabla[0])

while True:
    print(f"\n==================== ITERACIÓN {iteracion} ====================")
    
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
        print("\n¡Óptimo alcanzado! Todos los valores de la fila Z son no negativos.")
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

# ----------------------------------------------------------------------
# MOSTRAR RESULTADOS FINALES
# ----------------------------------------------------------------------
print("\n==================== SOLUCIÓN FINAL ====================")

# El valor óptimo de Z está en la última columna
zMax_optimo = tabla[0][-1]
print(f"El valor óptimo de la Función Objetivo Z es: {zMax_optimo:.4f}")

print("\nValores de las Variables:")

for i in range(1, len(laterales)):
    var_nombre = laterales[i]
    
    # Si la variable es una x (básica), su valor es el de la columna "Solución" en esa fila
    if var_nombre.startswith('x'):
        valor = tabla[i][-1]
        print(f"  {var_nombre} = {valor:.4f}")

# Las variables que no están en la lista 'laterales' (no básicas) tienen valor 0.