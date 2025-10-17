
print("Hola mundo")
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


tabla_inicial = [] #inicializamos una lista
funcion_objetivo = []

print("\n-- Función Objetivo (ingresa los coeficientes de la función a maximizar) --")

# FILA DE LA FUNCIÓN OBJETIVO (Z)
print(f"\nFila '{laterales[0]}':") #mostramos encabezados
fila_z = [] # Usamos fila_z para más claridad
for j in range(len(encabezados)):
        if j < variables:
            # Pide coeficientes de variables originales
            valor = float(input(f"  {encabezados[j]}    = "))
            fila_z.append(valor)
        else:
            #despues de las variables, las s de holgura y la solución son 0
            fila_z.append(0.0)
tabla_inicial.append(fila_z)


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
    tabla_inicial.append(fila)  #se agrega renglón por renglón

    

print("\nTABLA INICIAL:\n")
print("       ", end="")            #imprimimos los encabezados 
for e in encabezados:
    print(f"{e:^7}", end="")
print()


for i in range(len(laterales)):
    print(f"{laterales[i]:<5} |", end=" ")
    for valor in tabla_inicial[i]:
        # Usamos .2f para una mejor visualización de los decimales
        print(f"{valor:^7.2f}", end="") 
    print()