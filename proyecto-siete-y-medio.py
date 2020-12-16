###############IMPORTAMOS LAS LIBRERIAS QUE VAMOS A USAR#############
import random as r
import pymysql
import xml.etree.ElementTree as et

tree=et.parse('Cartas.xml')
root= tree.getroot()
cartas=[]                   #######Importamos las cartas y las reglas#############
cartas_backup=[]
for carta in root:
    cont=0
    for sub in carta:
        if cont == 0:
            id=sub.text
        elif cont == 1:
            valor=int(sub.text)
        elif cont == 2:
            palo=sub.text
        elif cont == 3:
            valor_j=float(sub.text)
        elif cont == 4:
            activa=sub.text
        cont+=1
    if activa=='SI':
        tupla=(valor,palo,valor_j)
        cartas.append(tupla)
        cartas_backup.append(tupla)
tree=et.parse('Basic_Config_Game.xml')
root= tree.getroot()
cont=0
for config in root:
    if cont==0:
        min_j=config.text
    elif cont==1:
        max_j=config.text
    elif cont==2:
        max_r=config.text
    elif cont==3:
        init_points=config.text
    elif cont==4:
        auto_mode=config.text
    cont+=1

#####################Definimos las pausas entre acciones y turnos###########
def intermedio():
    print()
    input('*****Pulsa intro*****')
    print()
#############Creamos una función para que detecte si se le permite apostar o no (dependiendo del % para superar el 7'5)#############
def puede_apostar(lista_de_cartas,puntuacion_cartas):
    save=0
    lost=0
    for i in lista_de_cartas:
        if puntuacion_cartas+i[2]>7.5:
            lost+=1
        else:
            save+=1
    if lost>save:
        return 'no'
    else:
        return 'si'

################Definimos como apuestan los bots###########
def apuesta_bot(puntos_restantes_bot,limite):
    apuesta2=False
    if limite[1]>puntos_restantes_bot:
        max=int(puntos_restantes_bot)
    else:
        max=limite[1]
    if limite[0]>puntos_restantes_bot:
        apuesta=puntos_restantes_bot
        apuesta2=True
    elif puntos_restantes_bot*1/5>limite[0]:
        min=int(puntos_restantes_bot*1/5)
    else:
        min=limite[0]
    if puntos_restantes_bot//5>limite[1]:
        apuesta=limite[1]
        apuesta2=True
    if not apuesta2:
        apuesta=r.randint(min,max)
    print('Apuesta: ', apuesta)
    return apuesta

# Lista de tuplas cartas
# mazo =[( valor real , prioridad , valor en el juego )]
limit=[2,5],[3,7],[4,9],[6,12] #[minimo,maximo]
palos_prio={'Oros':1, 'Copas':2, 'Espadas':3, 'Bastos':4}
cartas=[(1,'Oros',1),(2,'Oros',2),(3,'Oros',3),(4,'Oros',4),(5,'Oros',5),(6,'Oros',6),(7,'Oros',7),(8,'Oros',8),(9,'Oros',9),(10,'Oros',0.5),(11,'Oros',0.5),(12,'Oros',0.5),
        (1,'Copas',1),(2,'Copas',2),(3,'Copas',3),(4,'Copas',4),(5,'Copas',5),(6,'Copas',6),(7,'Copas',7),(8,'Copas',8),(9,'Copas',9),(10,'Copas',0.5),(11,'Copas',0.5),(12,'Copas',0.5),
        (1,'Espadas',1),(2,'Espadas',2),(3,'Espadas',3),(4,'Espadas',4),(5,'Espadas',5),(6,'Espadas',6),(7,'Espadas',7),(8,'Espadas',8),(9,'Espadas',9),(10,'Espadas',0.5),(11,'Espadas',0.5),(12,'Espadas',0.5),
        (1,'Bastos',1),(2,'Bastos',2),(3,'Bastos',3),(4,'Bastos',4),(5,'Bastos',5),(6,'Bastos',6),(7,'Bastos',7),(8,'Bastos',8),(9,'Bastos',9),(10,'Bastos',0.5),(11,'Bastos',0.5),(12,'Bastos',0.5)]
cartas_backup=[(1,'Oros',1),(2,'Oros',2),(3,'Oros',3),(4,'Oros',4),(5,'Oros',5),(6,'Oros',6),(7,'Oros',7),(8,'Oros',8),(9,'Oros',9),(10,'Oros',0.5),(11,'Oros',0.5),(12,'Oros',0.5),
               (1,'Copas',1),(2,'Copas',2),(3,'Copas',3),(4,'Copas',4),(5,'Copas',5),(6,'Copas',6),(7,'Copas',7),(8,'Copas',8),(9,'Copas',9),(10,'Copas',0.5),(11,'Copas',0.5),(12,'Copas',0.5),
               (1,'Espadas',1),(2,'Espadas',2),(3,'Espadas',3),(4,'Espadas',4),(5,'Espadas',5),(6,'Espadas',6),(7,'Espadas',7),(8,'Espadas',8),(9,'Espadas',9),(10,'Espadas',0.5),(11,'Espadas',0.5),(12,'Espadas',0.5),
               (1,'Bastos',1),(2,'Bastos',2),(3,'Bastos',3),(4,'Bastos',4),(5,'Bastos',5),(6,'Bastos',6),(7,'Bastos',7),(8,'Bastos',8),(9,'Bastos',9),(10,'Bastos',0.5),(11,'Bastos',0.5),(12,'Bastos',0.5)]

###################Retiramos las cartas que no vamos a utilizar###########################
remove=((8,'Oros',8),(8,'Copas',8),(8,'Espadas',8),(8,'Bastos',8),(9,'Oros',9),(9,'Copas',9),(9,'Espadas',9),(9,'Bastos',9))
for i in remove:
    cartas.remove(i)
    cartas_backup.remove(i)
# Hacer lista de jugador max 8
############Definimos los jugadores que van a participar y cuales serán bots##################################3
def usuarios():
    global jugadores
    while 1==1:
        bots=input('Quieres jugar con bots? (Si/No): ').upper()             #Preguntamos si quiere jugar con bots
        if bots=='SI' or bots=='NO':
            break
        else:
            print('Si quieres hcaer la elección, introduce Si o No')
    if bots=='NO':
        jugadores=[]
        while 1==1:                                                                 #Si no queremos jugar con bots ..

                try:
                    numj=int(input('Introduce el numero de jugadores HUMANOS, máximo 8: '))     #preguntamos cuantos jugadores habrá.
                    if numj != 1 and numj>0 and numj<8 :                                        #nos aseguramos que solo pueda introducir un num entre 2-8
                        break
                    else:
                        print(f'No puedes jugar solo o con {numj} jagadores')
                    if numj>8 or numj<0:
                        print('El dato introducido no es valido')
                except:
                    print('Tienes que introducir un numero')

        for i in range(numj):
            while 1==1:
                nombre=input("Escribe el nombre del juagdor: ")                                 #pedimos el nombre de los jugadores
                if nombre[:3]=='bot':                                                           #impedimos que el jugadore se llame bot para poder distinguir al jugador de la máquina
                    print('El nombre del jugador no puede contener bot al inicio de su nombre')
                elif nombre.isalnum()==True and nombre[0].isalpha()==True:                      #si el nombre cumple con las condicciones, lo introducimos a la lista de jugadores
                    jugadores.append(nombre)
                    break
                elif nombre.isalnum()==False:
                    print("El nombre tiene que estar compuesto por letras y numeros, no puede contener espacios.")
                elif nombre[0].isalpha()==False:
                    print("El primer carácter del nombre tiene que ser una letra.")
    elif bots=='SI':
        jugadores=[]
        while 1==1:
            try:
                numj=int(input('Introduce el numero de jugadores HUMANOS, máximo 7: ')) #pedimos el numero de los jugadores humanos, bajo ciertas condiciones
                if  numj > 0 and numj < 8:
                    break
                else:
                    print(f'No puedes jugar solo o con {numj} jagadores')
                if numj>8 or numj<0:
                    print('El dato introducido no es valido')
            except:
                print('Tienes que introducir un numero')
        for i in range(numj):
            while 1==1:
                nombre=input("Escribe el nombre del juagdor: ")                    #pedimos el nombre de los jugadores, bajo ciertas condiciones
                if nombre[:3]=='bot':
                    print('El nombre del jugador no puede contener bot al inicio de su nombre')
                elif nombre.isalnum()==True and nombre[0].isalpha()==True:
                    jugadores.append(nombre)
                    break
                elif nombre.isalnum()==False:
                    print("El nombre tiene que estar compuesto por letras y numeros, no puede contener espacios.")
                elif nombre[0].isalpha()==False:
                    print("El primer carácter del nombre tiene que ser una letra.")
        numbmax=8-numj                                                          #Actualizamos el num. max de jugadores
        while 1==1:
            try:
                numb=int(input(f'Con cuantos bots quieres jugar, el máximo de jugadores es {numbmax}: ')) #pedimos con cuantos bots quieres jugar
                if numb != 1 and numb > 0 and numb < numbmax:                                                  #solo puede introducir x num de bots
                    break
                else:
                    print(f'No puedes introducir {numb} bots')
                if numb>8 or numb<0:
                    print('El dato introducido no es valido')

            except:
                print('Tienes que introducir un numero')
        for i in range(numb):                                                                       #introducimos los bots en la lista
            jugadores.append(f'bot{i}')
###########################ORDEN_JUGADORES(bucle 0)###################################
# Escoger carta aleatoria por jugador para orden prioridad, Bucle nueva mano 0
def orden_jugadores():
    global jugadores
    global cartas
    for i in range(len(jugadores)):     #bucle para dar 1 carta a cada jugador        #para que no se repitan las cartas
        carta=r.choice(cartas)
        print(f'El juagdor {jugadores[i]}\nsaca {carta[0]} de {carta[1]} ')
        cartas.remove(carta)
        jugadores[i]=jugadores[i],carta
    for i in range(len(jugadores)-1):   #ordeno x burbuha
        for j in range(len(jugadores)-1):
            k=j+1
            if jugadores[j][1][0]>jugadores[k][1][0]:
                aux=jugadores[j]
                jugadores[j]=jugadores[k]
                jugadores[k]=aux    #si el palo coincide gana el que tiene prioridad mas baja
    for i in range(1,len(jugadores)):
        if jugadores[i-1][1][0]==jugadores[i][1][0]:
            prio1=palos_prio[jugadores[i-1][1][1]]
            prio2=palos_prio[jugadores[i][1][1]]
            if prio1<prio2:
                aux=jugadores[i]
                jugadores[i]=jugadores[i-1]
                jugadores[i-1]=aux
    for i in range(len(jugadores)):         #le quito la carta a los jugadores
        jugadores[i]=jugadores[i][0]
    reset_mazo()

def reset_mazo():
    global cartas
    global cartas_backup
    cartas=[]
    for i in cartas_backup:  #reinicio el mazo
        cartas.append(i)
#####################INICIO_DICCIONARIO_JUG##################################
# Diccionario con tuplas de cada jugador (La clave es el nombre del jugador y los valores son una lista de elementos

#Bucle mano por jugador(1)
#######################BUCLE_MANO_JUGADOR(1)############################
def mano():
    global contmano
    global jugadores
    global jugador
    global limit

    cont=1
    contmano+=1
    print(f'mano {contmano}'.rjust(14))             #mostramos en que mano estamos
    if contmano < 30 * 1 / 4:                       #asignamos min y max dependidendo del estado de la partida
        limit_mano = limit[0]
    elif contmano < 30 * 1 / 2:
        limit_mano = limit[1]
    elif contmano < 30 * 3 / 4:
        limit_mano = limit[2]
    else:
        limit_mano = limit[3]

    for i in jugadores:
        if cont!=len(jugadores):    #asignamos una prioridad al jugador
            jugador[i][3]=cont
        else:
            jugador[i][3]=0         #asignamos la banca al jugador
        if jugador[i][2]=='eliminado':  #avisamos que el jugador esta eliminado
            print(f'El jugador {i} esta Eliminado')
        else:                           #si no esta eliminado..
            if jugador[i][3]==0:            #printamos el nombre del jugador
                print(f'Turno de {i} es la banca')
            else:
                print(f'Es el turno de {i}')
            print(f'\tTienes {jugador[i][6]} puntos') #printamos cuantos puntos tienes
            carta_r = r.choice(cartas)                #coges una carta
            cartas.remove(carta_r)                    #se borra de la lista de cartas posibles
            print(f'\tHa robado {carta_r[0]} de {carta_r[1]}') #mostramos la carta robada
            jugador[i][0] = carta_r                    #se le asigna la carta
            jugador[i][4] = carta_r[2]                 # se le asigna el valor de la carta
            print(f'\tValor de la mano: {jugador[i][4]}'.rjust(5)) # se muestra el valor de los puntos de tu mano
            jugador[i][7] = contmano                    #asignamos el num de mano al jugador
            jugador[i][2] = 'jugando'                   #el jugador juega la mano
            jugador[i][1] = 'jugando'                   # el jugador juega la partida
        if i[:3]=='bot'and jugador[i][3]!=0:            #un bot que no es la banca..
            print(f'Limite de apuesta para bot: {limit_mano[0]} a {limit_mano[1]}') #mostramos los puntos que puede apostar
            if puede_apostar(cartas,jugador[i][4]): #si puede apostar...
                jugador[i][5]=apuesta_bot(jugador[i][6],limit_mano) #el bot apuesta
                while 1==1 and puede_apostar(cartas,jugador[i][4]):
                    save=0
                    lost=0
                    for h in cartas:
                        if jugador[i][4]+h[2]>7.5:
                            lost+=1
                        else:
                            save+=1
                    survive=save+lost
                    if save*100/survive>=65:                             #si tiene + de 65% de posibilidades de no pasarse de 7'5 sigue jugando (robar)
                        jugador[i][1]='jugando'
                    elif save*100/survive>=50 and save*100/survive<65: #si tiene + de 50% o -65% de posibilidades de no pasarse de 7'5 tiene ese porcentaje de seguir jugando (robar) sino se planta
                        valor=r.randint(1,100)
                        if valor<=save*100/survive:
                            jugador[i][1]='jugando'
                            print('Sigue jugando')

                        else:
                            jugador[i][1]='plantado'
                            print('Se planta')

                    elif save*100/survive<50:                       #si tiene -50% de posibilidades de no pasarse de 7'5 tiene ese porcentaja entre tres de seguir jugando (robar) sino se planta
                        valor=r.randint(1,100)
                        if valor<=(save*100/survive)/3:
                            jugador[i][1]='jugando'
                            print('Sigue jugando')
                        else:
                            jugador[i][1]='plantado'
                            print('Se planta')

                    if jugador[i][1]=='jugando':                #el jugador humano..
                        carta_r = r.choice(cartas)              #roba carta
                        cartas.remove(carta_r)                  #se quita la carta del mazo
                        print(f'\tHa robado {carta_r[0]} de {carta_r[1]}')  #muestras la carta robada
                        jugador[i][4] += carta_r[2]             #le asignas la carta al jugador
                        print('\tValor de la mano: ', jugador[i][4])    #muestra el valor de la mano actual
                        if jugador[i][4] > 7.5:                 #si el jugador se pasa de 7'5 queda eliminado de la mano
                            jugador[i][1] = 'eliminado'
                            print('Te has pasado de 7 y medio')
                            break
                    if jugador[i][1]=='plantado':              #el jugador se planta
                        break

            else:                                              #el bot apuesta y se planta
                jugador[i][5]=apuesta_bot(jugador[i][6],limit_mano)
                jugador[i][1]='plantado'
        elif puede_apostar(cartas,jugador[i][4]) and jugador[i][3]!=0: #si el jugador Humano puede apostar y no es la banca...
            # apostado = False
            # min=jugador[i][6]//5
            # if limit_mano[1] > jugador[i][6]:
            #     max = jugador[i][6]
            # else:
            #     max = limit_mano[1]
            # if limit_mano[0] > jugador[i][6]:
            #     apuesta = jugador[i][6]
            #     print(f'Apuesta - {apuesta} puntos')
            #     apostado=True
            # elif jugador[i][6] * 1 / 5 > limit_mano[0]:
            #     min = jugador[i][6] * 1 / 5
            # else:
            #     min = limit_mano[0]
            # if jugador[i][6]//5 >limit_mano[1]:
            #     apuesta= limit_mano[1]
            #     print(f'Apuesta - {apuesta}')
            #     apostado=True
            while 1==1 :
                try:
                    jugador[i][5]=int(input(f'Introduce la apuesta que quieres realizar: '))    #haces la apuesta con los puntos que tengas

                    if jugador[i][5]<0 :
                         print('No se puede apostar menor ha cero')
                        # elif jugador[i][5]>max:
                        #    print('No se puede apostar mas del maximo')
                    elif jugador[i][5]>20:
                        print('No puedes gastar mas puntos de los que tienes')

                    else:
                        break
                except:
                        print('Solo se acepta un numero como apuesta')
            while 1==1 and jugador[i][1]!='eliminado':                  #si el jugador no esta eliminado..
                if puede_apostar(cartas,jugador[i][4])=='si':       #si puedes seguir robando...
                    while 1==1:
                        try:
                            estado=int(input('Que quieres hacer:\n1)Plantarte\n2)Seguir\n'))    #decides que quieres hacer en un turno
                            break
                        except:
                            print(f'Decide que quieres hacer')
                    if estado==1:               #se planta
                        jugador[i][1]='plantado'
                        break
                    elif estado==2:             #sigue jugando
                        jugador[i][1]='jugando'
                        while 1==1:
                            carta_r = r.choice(cartas)      #roba carta
                            cartas.remove(carta_r)          #se quita la carta del mazo
                            print(f'\tHa robado {carta_r[0]} de {carta_r[1]}') #se muestra la carta robada
                            jugador[i][4]+=carta_r[2]       #se le asigna la carta robada al jugador
                            print('\tValor de la mano ',jugador[i][4])  #se muestra el valor de la mano actual
                            if jugador[i][4]>7.5:           #si el valor de la mano supera 7'5 queda eliminado ese turno
                                jugador[i][1]='eliminado'
                                print('Te has pasado de 7 y medio')
                                break
                            else:
                                break
                    else:
                        print('El dato introducido no es valido')
                elif  puede_apostar(cartas,jugador[i][4])=='no':    #si no puedes seguir robando te plantas
                    jugador[i][1]='plantado'
                    print('Te plantas')
                    break
        if jugador[i][3]==0 and i[:3]=='bot':       #si el jugador es un bot y es la banca..
            while 1==1:
                cosa=0
                for h in jugadores:

                    if jugador[h][4]>cosa and jugador[h][4]<7.5 :   #guardamos el jugador el valor de la mano mas alto
                        cosa=jugador[h][4]
                if jugador[i][4]<cosa and jugador[h][4]<=7.5:       #la banca sigue robando hasta superar o igualar el valor de mano mas alto de los demás jugadores sino se planta
                    jugador[i][1] = 'jugando'
                else:
                    jugador[i][1]='plantado'

                if jugador[i][1] == 'jugando':      #si la vanca sigue jugando..
                    print('Sigue jugando')
                    carta_r = r.choice(cartas)      #roba una carta
                    cartas.remove(carta_r)          #se elimina de la mano
                    print(f'\tHa robado {carta_r[0]} de {carta_r[1]}')  #muestra la carta robada
                    jugador[i][4] += carta_r[2]     #se le asigna la carta
                    print('\tValor de la mano ', jugador[i][4])     #muestra el valor de la mano
                    if jugador[i][4] > 7.5:         #si el valor de la mano es mas grande de 7'5 queda eliminado ese turno
                        jugador[i][1] = 'eliminado'
                        print('Te has pasado de 7 y medio')
                        break
                if jugador[i][1] == 'plantado': #se planta
                    print('Se planta')
                    break
        elif jugador[i][3]==0 and i[:3]!='bot':     #si el jugador Humano es la banca y no es un bot...
            while 1==1 and jugador[i][1]:
                while 1==1:
                    try:
                        estado=int(input('Que quieres hacer:\n1)Plantarte\n2)Seguir\n'))        #decides que quieres hacer
                        break
                    except:
                        print(f'Decide que quieres hacer')
                if estado == 1:         #se planta
                    jugador[i][1] = 'plantado'
                    break
                elif estado == 2:       #sigue jugando
                    jugador[i][1] = 'jugando'
                    while 1==1:
                        carta_r = r.choice(cartas)  #roba una carta
                        cartas.remove(carta_r)      #quitas la carta del mazo
                        print(f'\tHa robado {carta_r[0]} de {carta_r[1]}'.rjust(5))     #muestras las cartas robadas
                        jugador[i][4] += carta_r[2] #asignas la carta al jugador
                        print('\tValor de la mano ', jugador[i][4]) #muestras el valor de la mano actual
                        if jugador[i][4] > 7.5:     #si el valor de la mano actual supera el 7'5 queda eliminiado ese turno
                            jugador[i][1] = 'eliminado'
                            print('Te has pasado de 7 y medio')
                            break
                        else:
                            break
                    if jugador[i][1]=='eliminado':  #si el jugador el jugador esta eliminado no puede hacer nada
                        break
                else:
                    print('El dato introducido no es valido')
        jugador[i][6]-=jugador[i][5]            #se le quitan los puntos apostados al jugador
        cont+=1                                 #el contador suma uno
        intermedio()                            #introducimos una pausa
##########################COMPARACION_PUNTUACIONES########################################
#ver quien gana las apuestas
def apuestas():
    global jugador
    global jugadores
    global partida
    global ganador

    puntos_b=jugador[jugadores[-1]][4]      #asignamos el valor de la mano a la banca
    if puntos_b>7.5:        #si el valor de la mano es superior a 7'5 se resetean el valor a 0
        puntos_b=0
    sieteymedio=[]          #creamos una lista para los jugadores que consiguen sacar 7'5
    conseguido=False
    for i in jugadores[:-1]:        #recorremos la lista jugadores, menos el último valor
        if jugador[i][2]!='eliminado':  #si el jugador no esta eliminado ..
            puntos_J=jugador[i][4]
            if puntos_J>7.5:            #si el valor de la mano es mayor de siete y medio, se resetea a cero
                puntos_J=0
            if puntos_J>puntos_b and puntos_J==7.5:     #si los puntos del jugador son más grande que la banca e igual a 7'5...
                if jugador[jugadores[-1]][6]<jugador[i][5]*2:   #si los puntos de la banca son más pequeños que los puntos del jugador por dos...
                    jugador[i][6]+=jugador[jugadores[-1]][6]    #se suman los puntos restantes de la banca al jugador
                    jugador[jugadores[-1]][6]=0                 #los puntos de la banca se actualizan a cero
                else:                                   #sino...
                    jugador[i][6]+=jugador[i][5]*3              #los puntos del jugador son los puntos apostados por tres
                    jugador[jugadores[-1]][6]-=jugador[i][5]*2  #se le quitan los puntos a la banca
                print(f'El jugador {i} gana {jugador[i][5]*3} puntos')  #Muestra los putnos ganados
                jugador[i][5] = 0   #los puntos apostados se resetean
                sieteymedio.append([i,jugador[i][3]])   #se añade al jugador en la lista de siete y medio
                conseguido=True
            elif puntos_J>puntos_b:         #si los puntos del jugador son más grandes que los de la banca...
                if jugador[jugadores[-1]][6]-jugador[i][5]<0:   #si los puntos de la banca menos la apuesta del jugador es menor que 0...
                    jugador[i][6]+=jugador[jugadores[-1]][6]    #los puntos del jugador mas los puntos de la banca
                    jugador[jugadores[-1]][6]=0                 #los puntos de la banca se resetean a cero
                else:
                    jugador[i][6]+=jugador[i][5]*2              #a los puntos del jugador se le suma la apuesta por 2
                    jugador[jugadores[-1]][6]-=jugador[i][5]    # los puntos de la banca menos la apuesta del jugador

                if jugador[jugadores[-1]][6]==0:                #si la banca se queda sin puntos printa...
                    print(f'El jugador {i} se queda con todos los puntos restantes de {jugadores[-1]}')
                    break
                else:
                    print(f'El jugador {i} gana {jugador[i][5] *2 } puntos')    #muestra los puntos ganados
                jugador[i][5] = 0                                               #la puesta del jugador se resetea
            else:           #sino...
                jugador[jugadores[-1]][6]+=jugador[i][5]          #la banca suma la apuesta del jugador
                print(f'La banca ({jugadores[-1]}) gana {jugador[i][5]} puntos') #muestra los puntos ganados por la banca
                jugador[i][5] = 0                                                  #la apuesta se resetea a 0
    #nuevas prioridades y banca,
    if conseguido:          #si alguien ha conseguido 7'5 (encaso de empate depende de la prio del juagdor) se elimina de la lista y se introduce de nuevo (por lo tanto se vuelve la banca)
        if len(sieteymedio)!=1:
            min=9 #como hay maximo 8 jugadores no va a haber una prioridad mayor a 9
            for i in range(sieteymedio):
                if sieteymedio[i][1]<min:
                    min=sieteymedio[i][1]
                    minpos=i
            sieteymedio=sieteymedio[minpos][0]
        if len(sieteymedio)==1:
            sieteymedio=sieteymedio[0][0]
        jugadores.remove(sieteymedio)
        jugadores.append(sieteymedio)
    for i in jugador:           #si el jugador no tiene puntos queda eliminado
        if jugador[i][6]<=0:
            jugador[i][2]='eliminado'
    eliminados=0
    for i in jugador:           #si los jugadores estan eliminados se suma a la variable elminiados, si los eliminados es igual a distáncia de la lsita menos una se acaba la partida
        if jugador[i][2]=='eliminado':
            eliminados+=1
        else:
            ganador=i           #el último jugador se guarda como ganador
    if eliminados==len(jugadores)-1:
        partida=False
####################################################################

#JUEGO#

while 1==1:                         #menú para elegir que quieres hacer
    while 1 == 1:
        try:
            opcion = int(input('1.-Jugar\n2.-Informes\n3.-Salir\nSelecciona una de las opciones: '))
            if opcion != 1 and opcion != 2 and opcion != 3:
                continue
            else:
                break
        except:
            print('Tienes que introducir un valor')
    if opcion==1:       #si eliges la opción jugar...
        partida = True
        usuarios()              #llamamos a las funciones para introducir jugadores y ordenarlos
        orden_jugadores()
        intermedio()
        jugador = {}        #hacemos un diccionario con la siguiente info
        for i in jugadores:
            jugador[i] = ['1ra_carta', 'estado mano actual', 'estado partida', 'prioridad', 'valor cartas', 0, 20,
                          'contador mano', ]
        contmano = 0        # iniciamos el contador de la mano a cero
        while contmano <= 30 and partida:       #mientras el numero de manos se menor o igual a 30 y mientras partida=True se juega una partida
            mano()
            apuestas()
            reset_mazo()
            intermedio()
        if not partida:                     #si la partida se ha acabado muestra el ganador
            print(f'El jugador {ganador} ha ganado')
        else:                               #si la partida llega a 30 turnos muestra el jugador con más puntos
            max = 0
            for i in jugador.keys():
                if jugador[i][6] > max:
                    max = jugador[i][6]
                    ganador = i
            print(f'El jugador {ganador} ha ganado')
    elif opcion==2:
        ############### CONFIGURAR ESTO ###################

        # Conexión de base de datos.
        conexion = "aws-carlos-basededatos.ccaui2eoe11e.us-east-1.rds.amazonaws.com"  # aquí pondremos nuestra dirección de la base de datos de Amazon web services
        usuario = "admin"  # usuario de la conexión
        password = "Alumne1234"  # contraseña
        BBDD = "proyecto"  # base de datos a la cual nos vamos a conectar
        db = pymysql.connect(conexion, usuario, password, BBDD)
        ###############Querys#####################
        query_sql = [
            " /*1*/WITH MyRowSet AS (select idparticipante,carta_inicial,count(carta_inicial) as 'usos',ROW_NUMBER() OVER (PARTITION BY idparticipante) AS Primera_carta from turnos group by idparticipante,carta_inicial)SELECT * FROM MyRowSet WHERE Primera_carta = 1;",
            "/*2*/select nombre,max(apuesta) as 'apuesta_max',idpartida from ( select case when username is not null then usuario.username else descripcion end as nombre,max(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida where turnos.apuesta is not null group by partida.idpartida,username ) tabla where (apuesta,idpartida) in (select max(turnos.apuesta),partida.idpartida  as apuesta from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida group by partida.idpartida order by max(turnos.apuesta) desc);",
            "/*3*/select nombre,min(apuesta)as 'apuesta_min',idpartida from (select case when username is not null then usuario.username else descripcion end as nombre,min(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida where turnos.apuesta is not null group by partida.idpartida,username) tabla where (apuesta,idpartida) in (select min(turnos.apuesta),partida.idpartida  as apuesta from jugador left join bot on bot.idbot=jugador.idbot left join usuario on usuario.idusuario=jugador.idusuario inner join participante on jugador.idjugador=participante.id_jugador inner join turnos on participante.id_participante=turnos.idparticipante inner join partida on turnos.idpartida=partida.idpartida group by partida.idpartida order by min(turnos.apuesta) desc) group by idpartida;",
            "/*4*/;",
            "/*5*/;",
            "/*6*/;",
            "/*7*/;",
            "/*8*/select count(t.idturnos) as 'contador', p.idpartida from turnos t inner join partida p on p.idpartida = t.idpartida where t.puntos_inicio-t.puntos_final < 0 and es_banca=1 group by idpartida;",
            "/*9*/select count(es_banca) as 'Banca', p.idpartida from turnos t inner join partida p on p.idpartida = t.idpartida where es_banca=1 group by idpartida;",
            "/*10*/;",
            "/*11*/select avg(t.apuesta) as 'Media_de_las_apuestas', p.idpartida from turnos t inner join partida p on p.idpartida = t.idpartida group by idpartida;",
            "/*12*/;",
            "/*13*/select count(t.carta_inicial) as 'Num_cartas_iniciales', sum((select valor from cartas where idcartas = t.carta_inicial)) as  'Valor_de_las_cartas', p.idpartida from turnos t inner join partida p on p.idpartida = t.idpartida group by idpartida;",
            "/*14*/;"

        ]
        outfileName = "Resultadoquery.xml"  #generamos el documento xml
        with open(outfileName, "w") as outfile:
            outfile.write('<?xml version="1.0" ?>\n')
            outfile.write('<mydata>\n')
            print("Informe sobre las partidas")
            db = pymysql.connect(conexion, usuario, password, BBDD)
            cursor = db.cursor()

            for i in query_sql:
                cursor.execute(i)
                rows = cursor.fetchall()
                outfile.write('  <query>\n')
                for row in rows:
                    outfile.write('    <row>\n')
                    for index in range(len(row)):
                        outfile.write('       <{}>{}</{}>\n'.format(cursor.description[index][0], row[index],
                                                                    cursor.description[index][0]))
                    outfile.write('\n    </row>\n')
                outfile.write('  </query>\n')
            outfile.write('</mydata>\n')
            outfile.close()
        db.close()
        while 1==1:     #elegimos una query oara mostrar por pantalla
            tree = et.parse('Resultadoquery.xml')
            root = tree.getroot()
            count = 0
            while 1==1:
                try:
                    informe = int(
                        input("\n1) Mostrar la Carta inicial más repetida por cada jugador(mostrar nombre jugador y carta)"
                              "\n2) Jugador que realiza la apuesta más alta por partida. (Mostrar nombre jugador)"
                              "\n3) Jugador que realiza apuesta más baja por partida. (Mostrar nombre jugador)"
                              "\n4) Ratio  de turnos ganados por jugador en cada partida (%),mostrar columna Nombre jugador, Nombre partida, nueva columna 'porcentaje %'"
                              "\n5) Porcentaje de partidas ganadas Bots en general. Nueva columna 'porcentaje %'"
                              "\n6) Mostrar los datos de los jugadores y el tiempo que han durado sus partidas ganadas cuya puntuación obtenida es mayor que la media puntos de las partidas ganadas totales"
                              "\n7) Cuántas rondas se ganan en cada partida según el palo"
                              "\n8) Cuantas rondas gana la banca en cada partida"
                              "\n9) Cuántos usuarios han sido la banca en cada partida"
                              "\n10) Partida con la puntuación más alta final de todos los jugadores, mostrar nombre jugador, nombre partida,así como añadir una columna nueva en la que diga si ha ganado la partida o no"
                              "\n11) Calcular la apuesta media por partida"
                              "\n12) Mostrar los datos de los usuarios que no son bot, así como cual ha sido su última apuesta en cada partida que ha jugado"
                              "\n13) Calcular el valor total de las cartas y el numero total de cartas que se han dado inicialmente en las manos en la partida"
                              "\n14) Diferencia de puntos de los participantes de las partidas entre la ronda 1 y 5"
                              "\n15) Salir"
                              "\nEscoje una query: "))

                except:
                    print('Tienes que introducir un numero')
                else:
                    break
            if informe==15:
                break
            else:           #printamos la query seleccionada
                for child in root:
                    count += 1
                    if count == informe:
                        for row in child:
                            for j in row:
                                print(f"{j.tag}".rjust(17), end="")
                            break
                        print()
                        for row in child:
                            for j in row:
                                print(f"{j.text}".rjust(17), end="")
                            print()
    elif opcion==3:     #salimos del programa
        break