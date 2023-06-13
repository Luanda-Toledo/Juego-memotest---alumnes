import pygame
import time
import random
import tarjeta
from constantes import *

def crear_tablero():
    '''
    Crea una lista de tarjetas
    Retorna un dict tablero
    '''
    tablero = {}
    tablero["tarjetas"] = generar_lista_tarjetas()
    tablero["tiempo_ultimo_destape"] = 0
    tablero["primer_tarjeta_seleccionada"] = None
    tablero["segunda_tarjeta_seleccionada"] = None

    return tablero

def generar_lista_tarjetas()->list:
    '''
    Función que se encarga de generar una lista de tarjetas ordenada aleatoriamente
    El for x me recorre todas las posiciones de x usando de step el ancho de la tarjeta
    El for y me recorre todas las posiciones de x usando de step el alto de la tarjeta
    Por ende me va a generar la cantidad de tarjetas que le especifique anteriormente 
    ajustandose a la resolución de mi pantalla de manera dinámica
    Usa la función random.shuffle para generar de manera aleatoria los identificadores. Genera una lista de identificadores
    en donde se repiten dos veces el mismo ya que en un memotest se repiten dos veces la misma carta
    Retorna la lista de las tarjetas generadas
    '''
    lista_tarjetas = []
    indice = 0
    lista_id = generar_lista_ids_tarjetas() 
    print(lista_id)
    img_escondida = "00.png"

    for x in range(0, CANTIDAD_TARJETAS_H * ANCHO_TARJETA, ANCHO_TARJETA):
        for y in range(0, CANTIDAD_TARJETAS_V * ALTO_TARJETA, ALTO_TARJETA):
            img = "0{0}.png".format(lista_id[indice])
            id = lista_id[indice]
            nueva_tarjeta = tarjeta.crear_tarjeta(img, id, img_escondida, x, y)
            lista_tarjetas.append(nueva_tarjeta)
            indice += 1
    
    return lista_tarjetas

def generar_lista_ids_tarjetas():
    lista_id = list(range(1, CANTIDAD_TARJETAS_UNICAS+1)) #Creo una lista con todos los identificadores posibles
    lista_id.extend(list(range(1, CANTIDAD_TARJETAS_UNICAS+1))) #Extiendo esa lista con otra lista identica ya que hay dos tarjetas iguales en cada tablero (mismo identificador)
    random.seed(time.time())
    random.shuffle(lista_id) #Esos identificadores los desordeno de forma al azar
    return lista_id
    
def detectar_colision(tablero: dict, pos_xy: tuple) -> int  :
    '''
    verifica si existe una colision alguna tarjetas del tablero y la coordenada recibida como parametro
    Recibe como parametro el tablero y una tupla (X,Y)
    Retorna el identificador de la tarjeta que colisiono con el mouse y sino retorna None
    '''
    for tarjetas in tablero["tarjetas"]:
        if tarjetas["rectangulo"].collidepoint(pos_xy):

            if tarjetas["visible"] == False:
                if tablero["primer_tarjeta_seleccionada"] == None or tablero["segunda_tarjeta_seleccionada"] == None:
                    tarjetas["visible"] = True
            
            if tablero["primer_tarjeta_seleccionada"] == None:
                tablero["primer_tarjeta_seleccionada"] = tarjetas
                tablero["tiempo_ultimo_destape"] = pygame.time.get_ticks()

            elif tablero["segunda_tarjeta_seleccionada"] == None:
                tablero["segunda_tarjeta_seleccionada"] = tarjetas
    
    return tarjetas["identificador"]

def actualizar_tablero(tablero: dict) -> None:
    '''ALTO_TARJETA
    Verifica si es necesario actualizar el estado de alguna tarjeta, en funcion de su propio estado y el de las otras
    Recibe como parametro el tablero

    Una de las primeras cosas que debemos verificar es si paso más del tiempo permitido en 
    el que podemos tener una tarjeta visible. Para hacer esto debemos obtener el tiempo actual 
    mediante pygame.time.get_ticks() y luego calcular el tiempo transcurrido desde el ultimo destape.
      Esto lo podemos hacer calculando la diferencia que tenemos con el dato guardado en 
      tablero["tiempo_ultimo_destape"].

      
      
    '''
    tiempo_actual = pygame.time.get_ticks()
    

















def comprarar_tarjetas(tablero: dict) -> bool | None:
    '''
    Funcion que se encarga de encontrar un match en la selección de las tarjetas del usuario.
    Si el usuario selecciono dos tarjetas está función se encargara de verificar si el identificador 
    de las mismas corresponde si es así retorna True, sino False. 
    En caso de que no hayan dos tarjetas seleccionadas retorna None
    '''
    retorno = None
    if tablero["primer_tarjeta_seleccionada"] != None and tablero["segunda_tarjeta_seleccionada"] != None:
        retorno = False
        if tablero["primer_tarjeta_seleccionada"]["identificador"] == tablero["segunda_tarjeta_seleccionada"]["identificador"]:
            tarjeta.descubrir_tarjetas(tablero["tarjetas"], tablero["primer_tarjeta_seleccionada"]["identificador"])
            retorno = True

    return retorno

def dibujar_tablero(tablero: dict, pantalla_juego: pygame.Surface):
    '''
    Dibuja todos los elementos del tablero en la superficie recibida como parametro
    Recibe como parametro el tablero y la ventana principal
    Para lograr nuestro objetivo vamos a necesitar iterar la lista de tarjetas contenida 
    dentro del diccionario tablero y en función del valor de la clave visible de cada tarjeta
    debemos mostrar la superficie correspondiente a la tarjeta “dada vuelta” o la imagen correspondiente.
    '''
    for tarjeta in tablero["tarjetas"]:
        if tarjeta["visible"]:
            pantalla_juego.blit(tarjeta["superficie"], tarjeta["rectangulo"])
        else:
            pantalla_juego.blit(tarjeta["superficie_escondida"], tarjeta["rectangulo"])
    