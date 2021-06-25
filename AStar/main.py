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

tamBloque = 60
font=pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 14)
finished = False
mapa = None
closed = []
opened = []


app = wx.App(False)
anchoApp = 0


def initVentana(altura, ancho):
    global anchoApp
    anchoApp = ancho+300
    superficie = pygame.display.set_mode((ancho+300, altura))
    pygame.display.set_caption("Configuracion")
    superficie.fill(BLANCO)
    return superficie



def loop(superficie):
    global mapa, finished, closed, opened, tamBloque
    app = wx.App(False)
    
    run = True
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
                y = int(pos[1]/tamBloque)
                x = int(pos[0]/tamBloque)
                if finished:
                    if evento.key == pygame.K_RETURN:
                        selector = False
                        profundidad = False
                        finished = False
                        configurando = True
                        mapa.hardReset()
                        closed = []
                        opened = []
                        print("Saliendo porque mi reset no reseat el arbol")
                        exit()
                #Fase de configuracion
                elif configurando and not finished:
                    print("Fase de configuracion")
                    if evento.key == pygame.K_e:
                        print("Agregando agente tipo mono")
                        mapa.colocarJugador(x,y,"mono")
                    if evento.key == pygame.K_t:
                        print("Agregando agente tipo pulpo")
                        mapa.colocarJugador(x,y,"pulpo")
                    if evento.key == pygame.K_UP:
                        print("Editando tiles")
                        mapa.editarTiles(x,y,True)
                    if evento.key == pygame.K_DOWN:
                        print("Editando tiles")
                        mapa.editarTiles(x,y,False)
                    if evento.key == pygame.K_w:
                        print("Editando meta")
                        mapa.colocarMeta(x,y,False)
                    if evento.key == pygame.K_r:
                        mapa.hardReset()
                        closed = []
                        opened = []
                    #Salir de cualuqier config
                    if evento.key == pygame.K_RETURN:
                        if len(mapa.metas) == 0:
                            wx.MessageBox(' No hay metas', 'Warning', wx.OK | wx.ICON_INFORMATION)
                        if mapa.hayJugador() == True:
                             wx.MessageBox(' No hay agentes', 'Warning', wx.OK | wx.ICON_INFORMATION)
                        else:
                            mapa.crearGrafo()
                            configurando = False
                            print("configuracion OFF")
                            mapa.setOriginal()
                            mapa.crearMascara()
        
        if not configurando and not finished:
            #closed, opened, raiz, index, bandera, raizOriginal
            mapa.estrella(closed, opened, mapa.raiz, 0, mapa.raiz, 0)
            mapa.setAltura()
            mapa.raiz2Hoja(mapa.raiz)
            for j, c in enumerate(closed):
                for i, o in enumerate(opened):
                    if o.valor == c.valor:
                        del opened[i]

            # print("Arbol")
            # mapa.imprimirArbol(mapa.raiz)
            # print()

            if mapa.done:
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
            dibujarJugador(superficie, "A(0)")
            dibujarMetas(superficie)
        elif configurando == False or finished == True:
            dibujarMapa(superficie, 1)
            dibujarJugador(superficie, "-")
            dibujarMetas(superficie)
            

            
            dibujarTexto(superficie, mapa.rutaIdeal, opened)
            mapa.descubirAlrededores(closed)

        dibujarCuadricula(superficie)
        pygame.display.update()

        if run:
            f = Frame(None, mapa.costos)
            f.Show()
            app.MainLoop()
            run = False

#[(1, 12), (1, 13), (1, 14), (1, 15), (2, 15), (2, 14), (2, 13), (2, 12), (3, 12), (3, 11), (3, 10), (3, 9), (2, 9), (1, 9)]
def pintar(superficie):
    dibujarMapa(superficie, 1)
    dibujarCuadricula(superficie)
    pygame.display.update()
    pygame.time.wait(150)

def dibujarJugador(superficie, string):
    global mapa
    if mapa.jugador:
        superficie.blit(font.render("I", True, (0,0,0)), (mapa.jugador.x0*tamBloque+10, mapa.jugador.y0*tamBloque+30))
        if string == "A(0)":
            superficie.blit(font.render(string, True, (0,0,0)), (mapa.jugador.x*tamBloque+3, mapa.jugador.y*tamBloque+11))
        else:
            if mapa.jugador.getPosT() == mapa.metas[0]:
                superficie.blit(font.render("AF({})".format(mapa.jugador.costoA), True, (0,0,0)), (mapa.jugador.x*tamBloque+3, mapa.jugador.y*tamBloque+3))

def dibujarMetas(superficie):
    global mapa
    for meta in mapa.metas:
        superficie.blit(font.render("F", True, (0,0,0)), (meta.x*tamBloque+10, meta.y*tamBloque+30))
        mapa.mapa[meta.y][meta.x].setJuego2Mascara()
        
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

def dibujarTexto(superficie, closed, opened):
    global mapa
    #mapa.descubirAlrededores(closed)
    for i,datos in enumerate(closed):
        superficie.blit(font.render(("C({})".format(datos[1])), True, (0,0,0)), (datos[0][0]*tamBloque+11, datos[0][1]*tamBloque+3))
    # for i,datos in enumerate(opened):
    #         superficie.blit(font.render("O({})".format(datos.costoA), True, (0,0,0)), (datos.valor[0]*tamBloque+11, datos.valor[1]*tamBloque+3))
        
          
def main():
    global mapa
    mapa = Mapa("mapa2.txt")
    superficie = initVentana(mapa.h*tamBloque,mapa.b*tamBloque)
    loop(superficie)

main() 