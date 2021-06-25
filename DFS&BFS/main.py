import pygame
import sys
import copy
import wx
from Mapa import Mapa
from nodo import Nodo
from Texto import Frame
###
# Eddieson Cortes Larios
# Inteligencia Artificial Practica 2
# 3CV17
##

pygame.init()
NEGRO = (0, 0, 0)
GRIS = (160, 160, 160)
CAMINO = (210, 210, 210)
BLANCO = (255,255,255)
VERDE = (0,210,0)
ROJO = (210, 0, 0)
AZUL = (93, 173, 226)

tamBloque = 40
font=pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 20)
finished = False
mapa = None
visitados = []
decisiones = []
nodosNivel = []
index = 0
criterios = []
selector = False
profundidad = False

app = wx.App(False)
anchoApp = 0


#MANUAL_CURSOR = pygame.image.load('seleccion.png').convert_alpha()
def resolverLaberinto():
    pass

def initVentana(altura, ancho):
    global anchoApp
    anchoApp = ancho+300
    superficie = pygame.display.set_mode((ancho+300, altura))
    pygame.display.set_caption("Configuracion")
    superficie.fill(BLANCO)
    return superficie

def loop(superficie):
    global mapa, finished, visitados, decisiones, criterios, index, selector, nodosNivel
    f = Frame(None, 'Criterio de prioridad')
    configurando = True
    while True:
        instrucciones = pygame.image.load("instru.png").convert_alpha()
        superficie.blit(instrucciones, [anchoApp-300, 40])
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                pos = pygame.mouse.get_pos()
                color = superficie.get_at((pos[0], pos[1]))[:3]
                y = int(pos[1]/40)
                x = int(pos[0]/40)
                if finished:
                    if evento.key == pygame.K_RETURN:
                        selector = False
                        profundidad = False
                        finished = False
                        configurando = True
                        mapa.hardReset()
                        visitados = []
                        decisiones = []
                        print("Saliendo porque mi reset no reseat el arbol")
                        exit()
                #Fase de configuracion
                elif configurando and not finished:
                    print("Fase de configuracion")
                    if evento.key == pygame.K_e:
                        print("Editando posicion inicial")
                        mapa.colocarJugador(x,y)
                    if evento.key == pygame.K_q:
                        print("Editando tiles")
                        mapa.editarTiles(x,y)
                    if evento.key == pygame.K_w:
                        print("Editando meta")
                        mapa.colocarMeta(x,y)
                    if evento.key == pygame.K_r:
                        mapa.hardReset()
                        visitados = []
                        decisiones = []
                    #Salir de cualuqier config
                    if evento.key == pygame.K_RETURN:
                        if mapa.getNoMetas() == 0:
                            print("no de metas: {}".format(mapa.getNoMetas()))
                            wx.MessageBox(' No hay metas', 'Warning', wx.OK | wx.ICON_INFORMATION)
                        if mapa.hayJugador() == True:
                             wx.MessageBox(' No hay agentes', 'Warning', wx.OK | wx.ICON_INFORMATION)
                        else:
                            mapa.crearGrafo()
                            configurando = False
                            print("configuracion OFF")
                            mapa.setOriginal()
                            mapa.crearMascara()
        
        if not configurando and not finished and selector:
            #heroe (6,4)  princesa(11,8)
            #buscador (4,8)  buscado (5,7)
            if profundidad:
                mapa.profundidad(visitados, criterios[0], mapa.jugador.getPosT(), mapa.raiz, 1)
                print("arbol (profunidad): \n{}".format(visitados))
            else:
                mapa.construirArbol(visitados, criterios[0], mapa.jugador.getPosT(), mapa.raiz, 1)
                print("arbol (niveles):")
                niveles = mapa.ancho(visitados,mapa.raiz)
                visitados = []
                for nivel in niveles:
                    visitados = visitados + nivel
                

            mapa.setAltura()
            mapa.raiz2Hoja(mapa.raiz, profundidad)
            mapa.descubirAlrededores(visitados)
            # print("paso por paso")
            # print(mapa.pasos)
            mapa.quitarVisitado()
            resp = wx.MessageBox("Mostrar solucion paso a paso? :\n(No -> Se muestra nodo por nodo)", 'Info', wx.YES | wx.NO | wx.ICON_QUESTION)
            if resp == wx.YES:
                if profundidad:
                    for paso in mapa.pasos:
                        mapa.mover(paso[0],paso[1])
                        mapa.explorarTile(paso)
                        pintar(superficie)
                else:
                    for nodos in niveles:
                        for celda in nodos:
                            mapa.mover(celda[0],celda[1])
                            mapa.explorarTile(celda)
                            pintar(superficie)
            else:
                if profundidad:
                    for celda in visitados:
                        mapa.mover(celda[0],celda[1])
                        mapa.explorarTile(celda)
                        pintar(superficie)
                else:
                    for nodos in niveles:
                        for celda in nodos:
                            mapa.pintarJugador(celda[0],celda[1])
                            mapa.explorarTile(celda)
                        pintar(superficie)
                        mapa.quitarJugadores()
                        pintar(superficie)

                        


            if mapa.metas[0] in visitados:
                resp = wx.MessageBox('¡ Ganaste !\nPresiona Enter para reiniciar', 'Info', wx.OK | wx.ICON_INFORMATION)
                if resp == wx.OK:
                    finished = True
                    configurando = False
            else:
                resp = wx.MessageBox('¡No se encontro solucion!\nPresiona Enter para reiniciar', 'Info', wx.OK | wx.ICON_INFORMATION)
                if resp == wx.OK:
                    finished = True
                    configurando = False
        
        if configurando == True and finished == False:
            dibujarMapa(superficie, 0)
        elif configurando == False or finished == True:
            dibujarMapa(superficie, 1)
            dibujarVisitados(superficie)

        if not selector:
            nuevo = f.GetName()
            print("nuevo: {}".format(nuevo))
            nuevo = nuevo.replace(" ", "")
            nuevoList = nuevo.split(",")
            print("nuevo: {}".format(nuevoList))
            nuevoTupla = tuple(nuevoList)
            print("nuevo: {}".format(nuevoTupla))
            criterios.append(nuevoTupla)
            
            selector = True
            resp = wx.MessageBox("Quieres usar profundidad? (No: ancho)", 'Info', wx.YES | wx.NO | wx.ICON_QUESTION)
            if resp == wx.YES:
                profundidad = True
            else:
                profundidad = False

        dibujarCuadricula(superficie)
        pygame.display.update()


def pintar(superficie):
    dibujarMapa(superficie, 1)
    dibujarCuadricula(superficie)
    pygame.display.update()
    pygame.time.wait(150)

def dibujarMapa(superficie, cual):
    global mapa
    for i, fila in enumerate(mapa.mapa):
        for j, elemento in enumerate(fila):
            tile = pygame.Rect(j*tamBloque, i*tamBloque, tamBloque, tamBloque)
            if cual == 0:
                pygame.draw.rect(superficie, elemento.getColor(False), tile)
            else:
                pygame.draw.rect(superficie, elemento.getColor(True), tile)
            if elemento.juego == "%":
                if j == 0 and i>0:
                    superficie.blit(font.render(str(i), True, (0,0,0)), (j*tamBloque+11, i*tamBloque+10))
                if i == 0 and j>0:
                    superficie.blit(font.render(str(j), True, (0,0,0)), (j*tamBloque+11, i*tamBloque+10))

def dibujarCuadricula(superficie):
    global mapa
    for i in range(mapa.b):
        pygame.draw.line(superficie, NEGRO, (0, i*tamBloque), (mapa.b*tamBloque, i*tamBloque), 2)
    for i in range(mapa.h+1):
        pygame.draw.line(superficie, NEGRO, (i*tamBloque, 0), (i*tamBloque, mapa.h*tamBloque), 2)

def dibujarVisitados(superficie):
    global mapa, visitados
    for i,cuadro in enumerate(visitados):
        if i == 0:
            tile = pygame.Rect(cuadro[0]*tamBloque, cuadro[1]*tamBloque, tamBloque, tamBloque)
            pygame.draw.rect(superficie, VERDE, tile)
        else:
            tile = pygame.Rect(cuadro[0]*tamBloque, cuadro[1]*tamBloque, tamBloque, tamBloque)
            pygame.draw.rect(superficie, AZUL, tile)

        if  mapa.metas[0] == cuadro:
            tile = pygame.Rect(cuadro[0]*tamBloque, cuadro[1]*tamBloque, tamBloque, tamBloque)
            pygame.draw.rect(superficie, ROJO, tile)
          
def main():
    global mapa
    mapa = Mapa("mapa.txt")
    superficie = initVentana(mapa.h*tamBloque,mapa.b*tamBloque)
    loop(superficie)

main()