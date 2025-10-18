
import matplotlib.pyplot as plt
import numpy as np
import itertools


def nonegativos(matriz):#funcion para ver si ya se encontro una solucion (busca negativos en el renglon de z), mientras haya regresa false
    for i in range(len(col)-1):
        if matriz[0][i]<0:
            return False
    return True

def simplex(matriz,col,ren, it):
    
    encontrado=nonegativos(matriz)#de inicio verificamos si hay negativos en z

    while not encontrado:#mientras siga encontrando negativos se hara este while
        print()
        print(f"ITERACIÓN {it}")
        minz=999999 #creamos una variable min con un valor alto
        for i in range (len(col)-1):#en este for buscamos el minimo del renglon z
            if matriz[0][i]<minz:
                minz=matriz[0][i]
                colpiv=i #obtenemos el indice de la columna pivote

        # print ("columna pivote:",col[colpiv])
        columnapivote= [] #creamos una lista llamada columna pivote que nos servira para hacer cambios en la matriz

        for i in range (len(ren)):#metemos todos los valores de la columna pivote a la lista columnapivote
            columnapivote.append(matriz[i][colpiv])

        div=[] #creamos una lista de divisiones 
        indsol=len(col)-1 #guardamos el indice de la columna del sol en una variable
        for i in range (1,len(ren)): #hacemos la division de la solucion entre la columna pivote y guardamos los resultados en la lista div
            div.append(matriz[i][indsol]/matriz[i][colpiv])
        # print ("divisiones:",div)
        minr=99999 #establecemos un minimo que representara el min de las divisiones
        for i in range (len(div)): #recorremos todos los resultados de div y encontramos el mas pequeño que no sea negativo, y ese sera nuestro renglon pivote
            if div[i]>=0 and div[i]<minr:
                minr=div[i]
                renpiv=i+1 #le agregamos 1 porque no contamos el renglon z
        # print (ren)
        # print (renpiv)        
        # print ("renglon pivote:", ren[renpiv])
        elementopiv= matriz[renpiv][colpiv] #definimos la variable de renglon pivote
        # print ("elemento pivote", elementopiv)
        ren[renpiv]= col[colpiv] #cambiamos la variable del renglon pivote por la variable de la columna pivote
        for i in range (len(col)): #asignamos los nuevos valores del nuevo renglon pivote con la formula
            matriz[renpiv][i]=matriz[renpiv][i]/elementopiv
        # print (matriz) #solo cambia el renglon pivote nuevo
        for i in range (len(ren)): #asignamos nuevos valores a todos los demas renglones con la formula
            for j in range (len(col)):
                if(i!=renpiv):
                    matriz[i][j]=matriz[i][j]-(columnapivote[i]*matriz[renpiv][j]) 
        print("      | "+" | ".join(f"{c:^7}" for c in col)) #imprimimos las variables de las columnas
        print("-" * (len(col)*11))  #imprimimos una linea para separacion 
        for i, fila in enumerate(matriz):
            print(f"{ren[i]:<5} | " + " | ".join(f"{x:7.2f}" for x in fila))#imprimimos cada fila de la matriz con formato incluyendo las variables


        encontrado=nonegativos(matriz)#volvemos a llamar a la funcion para ver si hemos encontrado una solucion
        it=it+1#agregamos una iteracion

    return 0


def metodosimplex():
    print()
    print("MATRIZ INICIAL")

    # print (nonegativos(matriz))

    print("      | "+" | ".join(f"{c:^7}" for c in col)) #imprimimos las variables de las columnas
    print("-" * (len(col)*11))  #imprimimos una linea para separacion 
    for i, fila in enumerate(matriz):
        print(f"{ren[i]:<5} | " + " | ".join(f"{x:7.2f}" for x in fila))#imprimimos cada fila de la matriz con formato incluyendo las variables

    it=1 #representa el numero de iteraciones
    simplex(matriz, col,ren,it) #llamamos a la funcion que resuelve
    indsol=len(col)-1
    # print ("solucion final")
    # print (indsol)
    # print(ren)

    print()
    print ("SOLUCIONES")
    for i in range (len(ren)): #para imprimir cada variable con su resultado
        print (ren[i], "=", round(matriz[i][indsol], 2))#redondea para que unicmante salga ocn dos decimales
        for nombre in variables: #vamos a marcar las variables que si tienen resultados que no sean 0
            if(ren[i]==nombre):
                variables[nombre]=1

    for nombre in variables:#las variables que en el diccionario tienen un 0 son las que no tienen un valor asignado, por lo tanto
        if (variables[nombre]==0):
            print (nombre, "=", 0)    
    print()
   
def encontrarpuntos(valsx,valsy, res):
    intersecciones = [(0.0,0.0)] #agregamos el punto 0,0
    ind=range(len(valsx)) 
    for i, j in itertools.combinations(ind,2):#genera todas las combinaciones 
        parvar=np.array([[valsx[i],valsy[i]],[valsx[j],valsy[j]]])#guarda los 2 valores de ambas variables
        parres=np.array([res[i], res[j]])#guarda los valores de ambos resultados     
        try:
            solucion=np.linalg.solve(parvar, parres)#resuelve el sitema de matrices
            xenint,yenint=solucion[0],solucion[1]#guradamos los valores
            if(xenint >= -1e-6 and yenint >= -1e-6):#si esta en el primer cuadrante (1e-6 por el redondeo)
                intersecciones.append((xenint, yenint))
        except np.linalg.LinAlgError:#si las lineas llegan a ser paralelas
            pass 

    # buscamos intersecciones con el eje x
    for i in range(len(valsx)):
        coe=valsx[i] # coeficientesx
        r=res[i]        
        #si la linea no es horizonal lo agregamos
        if (abs(coe)>1e-6 and r>=0):
            intx =r/coe
            if intx >= -1e-6: # Que caiga en el cuadrante positivo
                intersecciones.append((intx, 0.0))

    # interseciones con el eje y
    for i in range(len(valsy)):
        coe=valsy[i] # coeficientesy
        r=res[i]    
        # si la linea no es vertical lo agregamos
        if (abs(coe)>1e-6 and r>=0):
            inty=r/coe
            if inty >= -1e-6: # Que caiga en el cuadrante positivo
                intersecciones.append((0.0,inty))
                
    # set para eliminar duplicados
    return list(set([(round(x,4),round(y,4)) for x,y in intersecciones]))


def metodografico():
    valsy=[] #para almacenar datos de la segundo variable
    res=[]#para almacenar los resultados 
    valsx=[] #para almacenar los datos de la primer varible 
    # print (len(matriz))

    for i in range (1,len(matriz)): #funcion para meter las varibles a las listas correspondientes
        # print ("restriccion")
        for j in range (len (matriz[i])):
            # print(matriz[i][j])
            if (j==0):#si esta en la columna 0 es valor de la primer variable
                valsx.append(matriz[i][j])
            elif(j==1):#si esta en la columna 1 es valor de la segunda variable
                valsy.append(matriz[i][j])
            elif(j==len(col)-1):#si esta en la ulitma columna es valor del resultado
                res.append(matriz[i][j])        
        
    # print (valsx, valsy, res)

    #buscar el maximo en x
    maxx=0 #buscamos la x maxima de todas las restricciones si y=0
    for i in range (len(valsx)):
        if (valsx[i]==0):
            maxx=maxx
        elif (res[i]/valsx[i]>maxx):
            maxx = res[i]/valsx[i]

    print (maxx) 

    maxy=0 #buscamos la y maxima de todas las restricciones si y¿x=0
    for i in range (len(valsy)): 
        if (valsy[i]==0):
            maxy=maxy
        elif (res[i]/valsy[i]>maxy):
            maxy = res[i]/valsy[i]

    print (maxy)  



    coloresgra=['plum','lightblue', 'blue','salmon',"firebrick","teal","olivedrab"]#definimos una lista de colores para la grafica
    plt.figure(figsize=(9, 7))#creamos la grafica

    yfac =1000000000#se inicializa con valor muy grande

    x= np.linspace(0, maxx, 200) # Genera 100 puntos de 0 al maximo en x

    for i in range (len(valsx)):
        color=coloresgra[i]
        y = (- valsx[i]*x+ res[i])/valsy[i]
        yfac = np.minimum(yfac, y)#se recorren todos los puntos de x y elige el valor mas pequeño de las ys
        #definimos que solo se vera en la grafica el cuadrante positivo por las restricciones de no negatividad
        cuadx= x[y >= 0]
        cuady =y[y >= 0]
        plt.plot(cuadx, cuady, label=fr'{valsx[i]}x + {valsy[i]}y = {res[i]}',color=color, linewidth=2)#creamos la linea con una etiqueta que tiene la funcion

        # for i in range (len(matriz)-1):
        #     print (i)




    puntos =encontrarpuntos(valsx,valsy,res)#buscamos todos los puntos en los que haya interseccion
    # print (puntos)

    puntosreal=[]#lista de puntos que entran en la solucion 
    # print("num res",  len(valsx))
    for i in range(len(puntos)):#en este for buscamos que puntos son los que cumplen con las restricciones para ver si son factibles o no
        var=0
        for j in range (len(valsx)):#recorremos por el numero de restricciones
            if(valsx[j]*puntos[i][0]+valsy[j]*puntos[i][1]<=res[j]): #RESTRICCIONES
                var+=1
                # print(valsx[j], puntos[i][0], " + ",valsy[j], puntos[i][1] , " <= " ,res[j])
                # print (var)
            if (var==len(valsx)):#si al final de recorrer toda la fila cumplio todas las restricciones lo metemos a la lista de puntos factibles
                puntosreal.append(puntos[i])   

    # print(puntosreal)


    colorpuntos=colores_pastel = ["gold","aquamarine","lightcoral", "rosybrown", "palegreen", "powderblue", "mediumpurple", "plum"]#lista de colores para graficar puntos

    
    #variables en los que guardaremos la solucion optima
    maxres=0
    masoptx=0.0 
    masopty=0.0 
    masoptres=0 
   
    for i in range(len(puntosreal)):
        #definimos valores de x y y redondeando 
        puntox=round(puntosreal[i][0],1)
        puntoy=round(puntosreal[i][1],1)
        # print (puntox,puntoy)
        plt.plot(puntox , puntoy, marker='o', markersize=10, color=colorpuntos[i], linestyle='', label=f'({puntox} , {puntoy})')#graficamos cada punto
        # print(matriz[0][0], puntox, " + ", matriz[0][1], puntoy,  " > ", maxres)
        if(matriz[0][0]*puntox+matriz[0][1]*puntoy>maxres):#buscamos el que nos de el mayor resultado porque esa es la solucion optima
            # print("entro")
            masoptx=puntox
            masopty=puntoy
            masoptres=matriz[0][0]*puntox+matriz[0][1]*puntoy
            maxres=matriz[0][0]*puntox+matriz[0][1]*puntoy

    # print(masoptx,masopty,masoptres)


    print("SOLUCION")#imprimimos los valores optimos que encontramos por cada variable
    print (f"{ren[0]}= {masoptres}" )
    print (f"{ren[1]}= {masoptx}" )
    print (f"{ren[2]}= {masopty}" )

    plt.fill_between(x,0,yfac,where=(yfac > 0),color='salmon',alpha=0.3,label='Región Factible')#rellenamos la region factible
    # Configuración de la gráfica
    plt.title('Método Gráfico',fontsize=14)
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.xlim(0,maxx*1.1) # marcamos el tamaño del eje x
    plt.ylim(0,maxy*1.1) # marcamos el tamaño del eje y
    plt.grid(True,linestyle='--',alpha=0.6)#pone la cuadricula
    plt.legend()
    nombre_archivo = "grafico_pauu.png"
    plt.savefig(nombre_archivo)

numvar =  int(input("¿Cuál es el número de variables? "))#pedimos el numero de variables y guardamos
numres =  int (input("¿Cuál es el número de restricciones? "))#pedimos el numero de restricciones y guardamos 

col=[] #lista que tendra los elementos de las columnas
ren=[]#lista que tendra los elementos de los renglones
variables={} #diccionario que tendra las variables con un 0 o 1 para identificar si fueron encontrados valores o no

for i in range(1,numvar+1):
    nomvar=  input(f"Nombre de la variable {i}? ")#preguntamos al usuario su nombre de su variable
    col.append(nomvar)#guardamos el nombre en las columnas
    variables[nomvar]=0 #guardamos el nombre en variables con el valor de 0

# for i in range(1,numvar+1):
#     col.append(f"x{i}")

for i in range(1,numres+1):#en este for metemos a la lista de columnas las variables de holgura, que dependen del numero de restricciones y las guardamos como S(NUM DE RESTRICCION)
    col.append(f"s{i}")#metemos esas variables a la lista de holgura 

col.append("Solución") #al final ingresamos la columna de solución
# print (col)

ren.append("z") #ingresamos el valor de Z en la lista de los renglones

for i in range(1,numres+1): #este for es para meter nuevamente las variables de holgura como S#
    ren.append(f"s{i}")
# print (ren)

matriz =[] #creamos una matriz que esta vacia

for i in range (len(ren)): #este bucle anidado nos sirve para ir llenando de valores la matriz, i recorre los renglones y j recorre las columnas
    if(i==0): #si estamos en el renglon 0 significa que estamos en la funcion objetivo
        fun="Funcion objetivo"
    else: #si estamos con algun otro valor signfica que estamos en un renglon de restricciones
        fun=f"Restricción {i}" 
    fila=[] #creamos una fila vacia para poder meter ahí los valores de cada renglon y asi meter la fila a la matriz

    for j in range (len(col)):
        if(j<numvar):#significa que estamos en una columna que tien una variable
            val = int(input(f"Ingresa el coeficiente de la variable {col[j]} de la {fun}: "))#pedimos que ingrese el coeficiente de la variable
            if(i==0):#si estamos en el renglon de z que es el renglon 0, los valores de la funcion objetivo se hacen negativos en la matriz
                fila.append(-val)
            else:    
                fila.append(val)

        elif(j==len(col)-1): #si estamos en la columna de solucion pedimos que meta el valor de la solucion
            if(i!=0):
                val = int(input(f"{fun} <= ")) 
                fila.append(val)
            else:
                fila.append(0)    

        else:#si no es parte de la solucion o de las variables se añaden los valores automaticamente a la matriz(son los las variables de holgura S1,S2...) 
            if (i==0):#si estamos en z todas las variables de holgura son 0
                val=0
                fila.append(val)
            else:
                if(j-(numvar-1)==i):#para poner los unos en la S de cada restriccion
                    val=1
                    fila.append(val)
                else:
                    val=0
                    fila.append(val)



    matriz.append(fila) #ya que tengamos el renglon con todos los valores lo ingresamos en la matriz y seguimos   


print ("¿Qué método quiere usar para resolver el problema")#preguntamos que metodo quiere usar
print("S - para método simplex ")
if (numvar==2):#si tiene 2 variables le damos la opcion de metodo grafico
    print("G - para método gráfico ")
metodo=input()#guardamos la decision del usuario




if (metodo=="S"): #si escogio s realizamos el metodo simplex
    metodosimplex()
elif(metodo=="G"):#si escogio g hacemos el cambio de variables en la funcion z ya que las habiamos puesto negativas y mandamos a llamar a la función
    matriz[0][0]=-matriz[0][0]
    matriz[0][1]=-matriz[0][1]
    metodografico()
else:#si por alguna razon se equivoco le damo otra oportunidad para meter bien el valor
    print ("¿Qué método quiere usar para resolver el problema")
    print("S - para método simplex ")
    if (numvar==2):
        print("G - para método gráfico ")
    metodo=input()

    if(metodo=="S"):
        metodosimplex()
    elif(metodo=="G"):
        matriz[0][0]=-matriz[0][0]
        matriz[0][1]=-matriz[0][1]
        metodografico()
    else:#si se vuelve a equivocar imprimimos error
        print("ERROR")    