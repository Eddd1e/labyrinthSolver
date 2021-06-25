from jugador import Jugador
from celda import Celda
from nodo import Nodo
from meta import Meta
import sys
import copy

class Mapa:

    def __init__(self, path):
        self.regresando = False
        self.raiz = None
        self.done = False
        self.mapa = []
        self.rutaIdeal = []
        self.letras= []
        self.h = 0
        self.b = 0
        self.altura = 0
        self.metas = []
        self.jugador = None
        self.grafo = {}
        self.costos = { # 2 1 -1 3
                "0": [-1, -1],
                "1": [2, 1],
                "2": [4, 2],
                "3": [3, 3],
                "4": [1, 4]
        }
        self.c = 0
        self.caminos = []

        f = open(path, "r")
        sys.setrecursionlimit(4000)
        lineas = f.readlines()
        for i, linea, in enumerate(lineas):
            celdas = []
            arr = linea.strip().split(",")
            for elem in arr:
                celdas.append(Celda(elem))
            self.mapa.append(celdas)
        self.h = len(lineas) + 1
        self.b = len(self.mapa[0]) + 1
        
        fila = []
        for i,filas in enumerate(self.mapa):
            self.mapa[i].insert(0,Celda("%"))

        for i in range(self.b):
            fila.append(Celda("%"))
        self.mapa.insert(0,fila)
        f.close()

    def metaContenida(self, meta):
        for elem in self.metas:
            
            if elem == meta:
                return True
        return False
        
    def borrarMeta(self, meta):
        self.metas = []

    def colocarJugador(self,x,y,tipo):
        if self.metas:
            if (x,y) != self.metas[0].getPosT():
                self.jugador = Jugador(x,y,tipo)
                return
        self.jugador = Jugador(x,y,tipo)
        
    def imprimir(self):
            for linea in self.mapa:
                for elem in linea:
                    print(elem.mascara, end="")
                print()

    def colocarMeta(self,x,y,opcional):
        self.borrarMeta((x,y))
        if self.jugador:
            if self.jugador.getPosT() != (x,y):
                self.metas.append(Meta(x,y,opcional))
                return
        self.metas.append(Meta(x,y,opcional))

    def hardReset(self):
        for linea in self.mapa:
            for e in linea:
                e.hardReset()
        self.jugador = None
        self.raiz = None
        self.metas = []
        self.grafo = {}

    def hayJugador(self):
        return self.jugador == None

    def setOriginal(self):
        for l in self.mapa:
            for e in l:
                e.setOriginal()

    def resetOriginal(self):
        for linea in self.mapa:
            for e in linea:
                e.resetOriginal()
        self.jugador.reiniciar()
        self.colocarJugador(self.jugador.x0, self.jugador.y0)

    def editarTiles(self,x,y,aumentar):
        valorActual = self.mapa[y][x].juego
        if aumentar:
            if int(valorActual) == 4:
                self.mapa[y][x].juego = "0"
            else:
                self.mapa[y][x].juego = str(int(self.mapa[y][x].juego) + 1)
        else:
            if int(valorActual) == 0:
                self.mapa[y][x].juego = "4"
            else:
                self.mapa[y][x].juego = str(int(self.mapa[y][x].juego) - 1)

    def crearMascara(self):
        self.mapa[self.jugador.y][self.jugador.x].setJuego2Mascara()
        if self.jugador.x > 1:
            self.mapa[self.jugador.y][self.jugador.x-1].setJuego2Mascara()
        if self.jugador.x < self.b-1:
            self.mapa[self.jugador.y][self.jugador.x+1].setJuego2Mascara()
        if self.jugador.y > 1:
            self.mapa[self.jugador.y-1][self.jugador.x].setJuego2Mascara()
        if self.jugador.y < self.h-1:
            self.mapa[self.jugador.y+1][self.jugador.x].setJuego2Mascara()

    def crearGrafo(self):
        for y,linea in enumerate(self.mapa):
            for x, elem in enumerate(linea):
                if x > 0 and y > 0:
                    self.grafo[(x,y)] = []

        for x,y in self.grafo.keys():
            if y < self.h-1:
                self.grafo[(x,y)].append( ( (x,y+1), self.mapa[y+1][x].juego) )
                self.grafo[(x,y+1)].append( ((x,y), self.mapa[y][x].juego) )
            if x < self.b-1:
                self.grafo[(x,y)].append( ( (x+1,y), self.mapa[y][x+1].juego) )
                self.grafo[(x+1,y)].append( ((x,y), self.mapa[y][x].juego) )

        self.raiz = Nodo((self.jugador.x,self.jugador.y), self.metas[0].getPosT(),0)
    
    def getAltura(self, raiz):
        if len(raiz.hijos) == 0:
            return 0
        else:
            maxH = 0;
            for hijo in raiz.hijos:
                maxH = max(maxH, self.getAltura(hijo))
            return maxH + 1;
        
    def setAltura(self):
        self.altura = self.getAltura(self.raiz)

    def imprimirArbol(self, raiz):
        print("({}, {})".format(raiz.valor, raiz.h), end="")
        for h in raiz.hijos:
            self.imprimirArbol(h)

    def raiz2Hoja(self, raiz):
        if raiz == None:
            return
        camino = [None]*(self.altura+1)
        self.construirCamino(raiz, camino, 0)
        for c in self.caminos:
            if self.metas[0].getPosT() in c:
                print("ruta ideal: ")
                costo = 0
                for nodo in c:
                    costo = costo + self.getCosto(self.mapa[nodo[1]][nodo[0]].juego)
                    self.rutaIdeal.append((nodo, costo))
                print(c)
                return
        print("No hay solucion")

    def construirCamino(self, raiz, camino, index):
        if raiz == None:
            return
        camino[index] = raiz.valor
        if len(raiz.hijos) == 0:
            self.guardarCaminos(camino, index)
        for hijo in raiz.hijos:
            self.construirCamino(hijo, camino, index+1)

    def guardarCaminos(self, camino, index):
        temp = []
        for i in range(index+1):
            temp.append(camino[i])
        self.caminos.append(temp)

    def borrarElemento(self, arr, raiz):
        for i,hijo in enumerate(arr):
            if hijo.equals(raiz):
                del arr[i]
                break

    def estrella(self, closed, opened, raiz, index, raizOriginal,count):
        self.c = count
        if count > 700:
            return
        if not self.estaEn(closed, raiz):
            self.raiz.estado = "C"
            self.jugador.mover(raiz.valor[0], raiz.valor[1])
            self.jugador.costoA = raiz.costoA
            closed.append(raiz)
            self.borrarElemento(opened, copy.deepcopy(raiz))
        if raiz.valor == self.metas[index].getPosT():
            print("meta encontrada")
            self.done = True
            return

        raiz.hijos = self.getCaminos(closed, raiz, opened)
        
        if len(opened)>0 and raiz.hijos:
            opened.sort(key=lambda x: (x.h, x.distanciaM, x.costoA))
            mejorOpened = self.find(raizOriginal, opened[0])
            
            for h in raiz.hijos:
                if not self.estaEn(closed, h) and not self.estaEn(opened, h):
                    opened.append(copy.deepcopy(h))
            try:
                if mejorOpened.mejorQue(raiz.hijos[0], self.metas[index].getPosT()):
                    print(mejorOpened.valor,mejorOpened.h ," mejor que: ", raiz.hijos[0].valor, raiz.hijos[0].h)
                    if not self.done and not self.c > 700:
                        self.estrella(closed, opened, mejorOpened, index, raizOriginal, count + 1)
            except None as e:
                #print(opened[0].valor, " not found")
                pass
            else:
                for h in raiz.hijos:
                    if not self.done and not self.c > 700:
                        self.estrella(closed, opened, h, index, raizOriginal,count + 1)
        else:
            for h in raiz.hijos:
                if not self.estaEn(closed, h) and not self.estaEn(opened, h):
                    opened.append(copy.deepcopy(h))
            for h in raiz.hijos:
                if not self.done and not self.c > 700:
                    self.estrella(closed, opened, h, index, raizOriginal,count + 1)
        

    def find(self, raiz, nodo):
        resultado = None
        if raiz.valor == nodo.valor and raiz.h==nodo.h:
            return raiz

        for h in raiz.hijos:
            resultado = self.find(h, nodo)
            if resultado !=None:
                break
        return resultado
        

    def getCosto(self, tipo):
        costo = self.costos[tipo]
        if self.jugador.tipo == "mono":
            return costo[0]
        elif self.jugador.tipo == "pulpo":
            return costo[1]
    
    def getCaminos(self, closed, raiz, opened):
        hijos = []
        #print("\tE:{} {} {} {}:".format(raiz.valor, raiz.h, raiz.distanciaM, raiz.costoA))
        
        for elem in self.grafo[raiz.valor]:
            costo = self.getCosto(elem[1])
            if int(costo) > -1:
                temp = Nodo(elem[0], self.metas[0].getPosT(), raiz.costoA+costo)
                if not self.estaEn(closed, temp):
                    hijos.append(Nodo(elem[0], self.metas[0].getPosT(), raiz.costoA+costo))
        hijos.sort(key=lambda x: (x.h, x.distanciaM, x.costoA))
        
        #for h in hijos:
        #    print("\t\t{} h:{} d:{} c:{}".format(h.valor,h.h ,h.distanciaM, h.costoA))
        return hijos

    def estaEn(self, closed, elem):
        for c in closed:
            if elem.equals(c):
                return True
        return False


    def descubirAlrededores(self, visitados):
        for casilla in visitados:
            if casilla.valor[0] > 1:
                self.mapa[casilla.valor[1]][casilla.valor[0]-1].setJuego2Mascara()
            if casilla.valor[0] < self.b-1:
                self.mapa[casilla.valor[1]][casilla.valor[0]+1].setJuego2Mascara()
            if casilla.valor[1] > 1:
                self.mapa[casilla.valor[1]-1][casilla.valor[0]].setJuego2Mascara()
            if casilla.valor[1] < self.h-1:
                self.mapa[casilla.valor[1]+1][casilla.valor[0]].setJuego2Mascara()

    def explorarTile(self, casilla):
        if casilla[0] > 1:
            self.mapa[casilla[1]][casilla[0]-1].setJuego2Mascara()
        if casilla[0] < self.b-1:
            self.mapa[casilla[1]][casilla[0]+1].setJuego2Mascara()
        if casilla[1] > 1:
            self.mapa[casilla[1]-1][casilla[0]].setJuego2Mascara()
        if casilla[1] < self.h-1:
            self.mapa[casilla[1]+1][casilla[0]].setJuego2Mascara()
