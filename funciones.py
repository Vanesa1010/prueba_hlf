import numpy as np
import variables as v

def crear_tableros():

    """
    Crea un tablero cuadrado lleno del carácter ("_").

    El tamaño se define en el archivo variables: tamanio.

    Devuelve:
            tablero de tamanio x tamanio con el carácter "_" en todas las casillas.
    """

    tablero = np.full((v.tamanio,v.tamanio), "_")

    return tablero


def buscar_inicio(eslora):

    """
    Elige al azar una orientación y una casilla inicial.
    Comprueba con la posición inicial si el barco entra o no.

    Repite el sorteo de la casilla hasta que el barco no se sale del tablero.

    Parámetros:
        -eslora (int): número de casillas del barco.

    Devuelve:
        -tuple: (orientacion, casilla_inicial), con orientacion "horizontal" o
        "vertical" y casilla_inicial como (fila, columna).
    """

    entra = False
    orientacion = np.random.choice(["horizontal", "vertical"])

    while entra == False:
        casilla_inicial = (np.random.randint(v.tamanio), np.random.randint(v.tamanio)) 
    
        if orientacion =="vertical":
            prueba_entra = casilla_inicial[0] + eslora -1
        
            if prueba_entra < v.tamanio:
                entra = True
                
            else:
                entra = False
            
        # orientación horizontal
        else:
            prueba_entra = casilla_inicial[1] + eslora -1
        
            if prueba_entra < v.tamanio:
                entra = True
            
            else:
                entra = False
            
  
    return orientacion, casilla_inicial



def crear_barco(eslora):

    """
    Genera las casillas de un barco aleatorio dentro del tablero.

    No comprueba si choca con otros barcos (eso lo hace la función esta_libre).

    Parámetros:
        -eslora (int): número de casillas del barco.

    Devuelve:
        -list: lista de tuplas (fila, columna), una por casilla del barco.
    """

    orientacion, casilla_inicial = buscar_inicio(eslora)
    
    barco = []

    for i in range(eslora):
        if orientacion == "vertical":
            casilla_nueva = (casilla_inicial[0]+i, casilla_inicial[1])
            barco.append(casilla_nueva)
        
        else:
            orientacion = "horizontal"
            casilla_nueva = (casilla_inicial[0], casilla_inicial[1]+i)
            barco.append(casilla_nueva)

    return barco  



def esta_libre(barco, tablero):

    """
    Comprueba que ninguna casilla del barco esté ya ocupada.

    Parámetros:
        -barco (list): casillas del barco como tuplas (fila, columna).
        -tablero (np.ndarray): tablero donde se quiere colocar.

    Devuelve:
        bool: -True si todas las casillas son "_"
              -False si alguna está ocupada.
    """

    for casilla in barco:

        if tablero[casilla] != "_":
            return False
       
    return True


def colocar_barco(barco, tablero):

    """
    Marca con "O" las casillas de un barco en el tablero.

    Modifica el tablero recibido.

    Parámetros:
        -barco (list): casillas del barco como tuplas (fila, columna).
        -tablero (np.ndarray): tablero donde colocarlo.

    Devuelve:
        -np.ndarray: el mismo tablero con el barco colocado.
    """

    for casilla in barco:
        tablero[casilla] = "O"

    return tablero    


def colocar_barcos(tablero):

    """
    Coloca la flota completa de forma aleatoria, sin solapamientos.

    La flota sale de variables.esloras. 
    
    Si un barco choca con otro, se genera uno nuevo hasta encontrar hueco.

    Parámetros:
        -tablero (np.ndarray): tablero vacío donde colocar los barcos.

    Devuelve:
        -np.ndarray: el mismo tablero con todos los barcos ("O").
    """


    esloras = v.esloras
    
    for eslora in esloras:
        barco = crear_barco(eslora) 
        
        while esta_libre(barco,tablero) == False:
                barco = crear_barco(eslora)

        colocar_barco(barco,tablero)
           
    return tablero


def disparar(casilla, tablero):

    """
    Dispara a una casilla y actualiza el tablero.

    "O" pasa a "X" (tocado), "_" pasa a "A" (agua). 
    Si la casilla ya tenía "X" o "A", no cambia nada.

    Parámetros:
        -casilla (tuple): (fila, columna) del disparo.
        -tablero (np.ndarray): tablero de barcos del objetivo.

    Devuelve:
        -str: "TOCADO", "AGUA" o "REPETIDO".
    """

    if tablero[casilla] == "O":
        tablero[casilla] = "X"
        return "TOCADO"

    elif tablero[casilla] == "_":
        tablero[casilla] = "A"
        return "AGUA"

    # para comprobar si ya se ha disparado
    else:
        return "REPETIDO"


def turnos(tablero_barcos_rival, tablero_disparos_rival, tablero_barcos_jugador, tablero_disparos_jugador):
    """
    Ejecuta la dinámica de turnos hasta que una flota queda hundida.

    Quien acierta repite turno.
    Quien falla (o repite casilla) pasa el turno.
    El jugador dispara por teclado y el rival al azar.

    Parámetros:
        -tablero_barcos_rival (np.ndarray): barcos de la máquina.
        -tablero_disparos_rival (np.ndarray): disparos de la máquina sobre ti.
        -tablero_barcos_jugador (np.ndarray): tus barcos.
        -tablero_disparos_jugador (np.ndarray): tus disparos sobre la máquina.

    Devuelve:
        -str: "Jugador" o "Rival", según quién gane.
    """

    ganador = ""

    # para pruebas que siempre empiece el jugador
    #turno = "jugador" 

    turno = np.random.choice(["jugador", "rival"])
    print("Empieza jugando el",turno)

    while "O" in tablero_barcos_jugador and "O" in tablero_barcos_rival: 
        if turno == "jugador":
            print("\n------ TU TURNO ------")
            print("Te toca disparar")
            
            fila = pedir_numero("Fila ")
            columna = pedir_numero("Columna ")
            casilla = (fila, columna)
            disparo_jugador = disparar(casilla, tablero_barcos_rival)
            print(f"Has disparado a {casilla}: {disparo_jugador}")
            tablero_disparos_jugador[casilla] = tablero_barcos_rival[casilla]
            
            pintar(tablero_disparos_jugador, tablero_barcos_rival)
            

            if disparo_jugador == "TOCADO":
                print("Has acertado. Continúas jugando")

            else: 
                print("No has acertado. Le toca jugar al rival")
                turno = "rival"

        else:
            print("\n------ TURNO DEL RIVAL ------")
            fila = np.random.randint(v.tamanio)
            columna = np.random.randint(v.tamanio)
            casilla_2 = (fila, columna)
            disparo_rival = disparar(casilla_2, tablero_barcos_jugador)
            print(f"El rival ha disparado a {casilla_2}: {disparo_rival}")
            tablero_disparos_rival[casilla_2] = tablero_barcos_jugador[casilla_2]
            print("\n------ DISPAROS RIVAL ------")
            print(tablero_disparos_rival)

            if disparo_rival == "TOCADO":
                    print("El rival ha acertado. Continúa jugando")
            
            else: 
                print("El rival no ha acertado. Te toca jugar")
                turno = "jugador"

    if "O" not in tablero_barcos_rival:
        ganador = "Jugador"
        print("¡¡ENHORABUENA!! Has ganado ;)")

    else:
        ganador = "Rival"
        print("Lo siento, ha ganado la máquina")

    return ganador        


def pintar(tablero_disparos_jugador, tablero_barcos_rival):
    """Muestra por pantalla el estado de la partida tras un disparo del jugador.

    Parámetros:
        -tablero_disparos_jugador (np.ndarray): lo que el jugador ha disparado.
        -tablero_barcos_rival (np.ndarray): barcos del rival (solo para pruebas).
    """

    print("\n------ TUS DISPAROS ------")
    print(tablero_disparos_jugador)
    print("\n------ COMPROBANDO BARCOS RIVAL ------")
    print(tablero_barcos_rival)


def pedir_numero(mensaje):

    """Pide un entero por teclado hasta que sea válido.

    Repite la pregunta si no es un número o está fuera del tablero
    (0 a tamanio - 1).

    Parámetros:
        -mensaje (str): texto que se muestra al pedir el dato.

    Devuelve:
        -int: número válido.
    """

    while True:
        try:
            numero = int(input(mensaje).strip())

        except ValueError:
            print("Eso no es un número entero")
        
        else:
            if 0 <= numero < v.tamanio:
                return numero
            print("El número tiene que estar entre 0 y {v.tamanio}")


def jugar(prueba=False):

    """Prepara una partida completa y la ejecuta.

    Crea los cuatro tableros, coloca los barcos, lanza turnos() y
    muestra el ganador.

    Parámetros:
        -prueba (bool): True para barcos a mano (partida corta),
        -False para barcos aleatorios.

    Devuelve:
        -str: "Jugador" o "Rival".
    """

    print("********** TABLEROS BARCOS **********")
    print("\n---------- TABLERO BARCOS JUGADOR --------")
    tablero_barcos_jugador = crear_tableros()
    print(tablero_barcos_jugador)
    print("\n---------- TABLERO BARCOS RIVAL ----------")
    tablero_barcos_rival = crear_tableros()
    print(tablero_barcos_rival)
    print("\n------- TABLERO DISPAROS JUGADOR ---------")
    tablero_disparos_jugador = crear_tableros()
    print(tablero_disparos_jugador)
    print("\n-------- TABLERO DISPAROS RIVAL ----------")
    tablero_disparos_rival = crear_tableros()
    print(tablero_disparos_rival)


    # barcos a mano para la prueba
    print("\n ********** AÑADIENDO LOS BARCOS AL TABLERO **********")

    tablero_barcos_rival[(0, 0)] = "O"
    print("\n---------- TABLERO BARCOS RIVAL ----------")
    print(tablero_barcos_rival)
    print("\n")
    print("\n---------- TABLERO BARCOS JUGADOR --------")
    tablero_barcos_jugador[(9, 9)] = "O"
    print(tablero_barcos_jugador)

    
    print("\n")
    print("\n---------- EMPIEZA EL JUEGO ----------")
    print("*****************************************")

    ganador_partida = turnos(tablero_barcos_rival, tablero_disparos_rival,
                            tablero_barcos_jugador, tablero_disparos_jugador)

    print("El ganador es: " + ganador_partida)