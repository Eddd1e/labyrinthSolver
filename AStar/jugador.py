class Jugador:
    def __init__(self,x,y,tipo):
        self.x = x
        self.y = y
        self.costoA = 0
        self.tipo = tipo
        self.x0 = x
        self.y0 = y
        self.visitados = [[x,y]]

    def mover(self, x, y):
        self.x = x
        self.y = y
        self.visitados.append([x,y])
        
    def reiniciar(self):
        self.x = self.x0
        self.y = self.y0
        self.visitados=[[self.x0,self.y0]]


    def getPosT(self):
        return (self.x, self.y)
