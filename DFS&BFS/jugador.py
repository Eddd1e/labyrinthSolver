class Jugador:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.x0 = x
        self.y0 = y
        self.movimientos = 0
        self.visitados = [[x,y]]

    def moverJugador(self, x, y):
        self.x = x
        self.y = y
        self.visitados.append([x,y])

    def regresar(self,x,y):
        self.x = x
        self.y = y
        
    def reiniciar(self):
        self.x = self.x0
        self.y = self.y0
        self.visitados=[[self.x0,self.y0]]
        self.movimientos = 0

    def agregarTile(self):
        self.visitados.append([self.x,self.y])
        self.movimientos = self.movimientos +1
    
    def getPos(self):
        return [self.x, self.y]

    def getPosT(self):
        return (self.x, self.y)
