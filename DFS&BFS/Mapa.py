from jugador import Jugador
from celda import Celda
from nodo import Nodo
import sys

class Mapa:
    def __init__(self, path):
        self.pasos = []
        self.raiz = None
        self.mapa = []
        self.h = 0
        self.b = 0
        self.altura = 0
        self.metas = []
        self.jugador = None
        self.grafo = {}
        self.caminos = []
        path = "mapa.txt"
        f = open(path, "r")
        sys.setrecursionlimit(2500)
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

    def metaContenida(self, meta):
        for elem in self.metas:
            if elem == meta:
                return True
        return False
        
    def borrarMeta(self, meta):
        for i,elem in enumerate(self.metas):
            if elem == meta:
                del self.metas[i]

    def colocarJugador(self,x,y):
        for i,linea in enumerate(self.mapa):
            for j,elem in enumerate(linea):
                if elem.isPlayer():
                    elem.resetOriginal()
                    break
        if self.mapa[y][x].juego == "1":  
            self.jugador = Jugador(x,y)
            self.raiz = Nodo((x,y), 1)
            self.mapa[y][x].setJuego("P")
            self.mapa[y][x].setMascara("P")
    def quitarVisitado(self):
        for i,linea in enumerate(self.mapa):
            for j,elem in enumerate(linea):
                if elem.mascara == "V":
                    elem.mascara = 1
                    return

    def mover(self,x,y):
        for i,linea in enumerate(self.mapa):
            for j,elem in enumerate(linea):
                if elem.isPlayer():
                    elem.resetVisitado()
                    break
        if self.mapa[y][x].juego != "0":  
            self.jugador = Jugador(x,y)
            self.mapa[y][x].setJuego("P")
            self.mapa[y][x].setMascara("P")
            
    def pintarJugador(self, x, y):
        self.mapa[y][x].setMascara("P")
        self.mapa[y][x].setJuego("P")

    def quitarJugadores(self):
        for i,linea in enumerate(self.mapa):
            for j,elem in enumerate(linea):
                if elem.isPlayer():
                    elem.resetVisitado()
                    

    def editarTiles(self,x,y):
        if self.mapa[y][x].juego == "0":
            self.mapa[y][x].setJuego("1")
        elif self.mapa[y][x].juego == "1":
            self.mapa[y][x].setJuego("0")

    def colocarMeta(self,x,y):
        if self.mapa[y][x].juego == "M":
           self.mapa[y][x].setJuego("1")
           self.borrarMeta((x,y))
        elif self.mapa[y][x].juego == "1":
            self.mapa[y][x].setJuego("M")
            self.metas.append((x,y))

    def hardReset(self):
        for linea in self.mapa:
            for e in linea:
                e.hardReset()
        self.jugador = None
        self.borrarArbol(self.raiz)
        self.metas = []
        self.grafo = {}

    def getNoMetas(self):
        return len(self.metas)

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

    def imprimir(self):
        for linea in self.mapa:
            for elem in linea:
                print(elem.mascara, end="")
            print()
        print(self.b,self.h)


    def crearMascara(self):
        self.mapa[self.jugador.y][self.jugador.x].mascara = "P"
        if self.jugador.x > 1:
            self.mapa[self.jugador.y][self.jugador.x-1].setJuego2Mascara()
        if self.jugador.x < self.b-1:
            self.mapa[self.jugador.y][self.jugador.x+1].setJuego2Mascara()
        if self.jugador.y > 1:
            self.mapa[self.jugador.y-1][self.jugador.x].setJuego2Mascara()
        if self.jugador.y < self.h-1:
            self.mapa[self.jugador.y+1][self.jugador.x].setJuego2Mascara()
    
    def descubrirAlrededor(self):
        self.mapa[self.jugador.y][self.jugador.x].mascara = "P"
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
                if x > 0 and y > 0 and self.mapa[y][x].juego != "0":
                    self.grafo[(x,y)] = []

        for x,y in self.grafo.keys():
            if y < self.h-1 and self.mapa[y+1][x].juego != "0":
                self.grafo[(x,y)].append( ("abj",(x,y+1)) )
                self.grafo[(x,y+1)].append( ("arr",(x,y)) )
            
            if x < self.b-1 and self.mapa[y][x+1].juego != "0":
                self.grafo[(x,y)].append( ("der",(x+1,y)) )
                self.grafo[(x+1,y)].append( ("izq",(x,y)) )
        
    
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

    def raiz2Hoja(self, raiz, profundidad):
        if raiz == None:
            return
        camino = [None]*(self.altura+1)
        self.construirCamino(raiz, camino, 0)
        for c in self.caminos:
            if self.metas[0] in c:
                if not profundidad:
                    for i, nodo in enumerate(c):
                        if nodo == self.metas[0]:
                            c = c[:i+1]
                print("ruta ideal: ")
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

    def profundidad(self, visitados, criterio, nodo, raiz, nivel):
        if nodo not in visitados:
            self.pasos.append(nodo)
            visitados.append(nodo)
            if self.metaContenida(nodo):
                return
            else:
                vecinos = self.grafo[(nodo)]
                for direccion in criterio:
                    for vecino in vecinos:
                        if direccion == vecino[0]:
                            valor = self.grafoMoverse(nodo, direccion)
                            hijo = Nodo(valor, nivel+1)
                            if valor not in visitados:
                                raiz.hijos.append(hijo)
                            self.profundidad(visitados, criterio, valor, hijo, nivel+1)
                            if self.metas[0] in visitados:
                                return
                            self.jugador.regresar(nodo[0], nodo[1])
                            if self.pasos[-1] != nodo:
                                self.pasos.append(nodo)
        else:
            return

    def construirArbol(self, visitados,criterio, nodo, raiz, nivel):
        if nodo not in visitados:
            visitados.append(nodo)
            if self.getVecinosNoVisitados(nodo, visitados) == 0:
                return
            else:
                vecinos = self.grafo[(nodo)]
                for direccion in criterio:
                    for vecino in vecinos:
                        if direccion == vecino[0]:
                            valor = self.grafoMoverse(nodo, direccion)
                            if valor not in visitados:
                                hijo = Nodo(valor, nivel+1)
                                raiz.hijos.append(hijo)
                                self.construirArbol(visitados, criterio, valor, hijo, nivel+1)
        
    def ancho(self, visitados, raiz):
        h = self.getAltura(self.raiz)+2
        niveles = []
        for i in range(1,h):
            nodos = []
            self.getNodosNiveles(self.raiz, i, nodos)

            if self.metas[0] in nodos:
                for x, nodo in enumerate(nodos):
                    if nodo == self.metas[0]:
                        nodos = nodos[:x+1]
                niveles.append(nodos)
                break
            niveles.append(nodos)

        for i, nodos in enumerate(niveles):
            print("nivel {}: {}".format(i+1, nodos))
        return niveles
        
    def getNodosNiveles(self, raiz, nivel, nodos):
        if raiz.nivel == nivel:
            nodos.append(raiz.valor)
            return
        elif raiz.nivel < nivel:
            for hijo in raiz.hijos:
                self.getNodosNiveles(hijo, nivel, nodos)

    def numVecinos(self, nodo):
        total = 0
        for d,coord in self.grafo[nodo]:
                total = total + 1
        return total

    def grafoMoverse(self, key, di):
        direcciones = self.grafo[key]
        for d in direcciones:
            if d[0] == di:
                return d[1]

    def descubirAlrededores(self, visitados):
        for casilla in visitados:
            if casilla[0] > 1:
                self.mapa[casilla[1]][casilla[0]-1].setJuego2Mascara()
            if casilla[0] < self.b-1:
                self.mapa[casilla[1]][casilla[0]+1].setJuego2Mascara()
            if casilla[1] > 1:
                self.mapa[casilla[1]-1][casilla[0]].setJuego2Mascara()
            if casilla[1] < self.h-1:
                self.mapa[casilla[1]+1][casilla[0]].setJuego2Mascara()

    def explorarTile(self, casilla):
        if casilla[0] > 1:
            self.mapa[casilla[1]][casilla[0]-1].setJuego2Mascara()
        if casilla[0] < self.b-1:
            self.mapa[casilla[1]][casilla[0]+1].setJuego2Mascara()
        if casilla[1] > 1:
            self.mapa[casilla[1]-1][casilla[0]].setJuego2Mascara()
        if casilla[1] < self.h-1:
            self.mapa[casilla[1]+1][casilla[0]].setJuego2Mascara()

    def getVecinosNoVisitados(self, key, visitados):
        total = 0
        for d,coord in self.grafo[key]:
            if coord not in visitados:
                total = total + 1
        return total