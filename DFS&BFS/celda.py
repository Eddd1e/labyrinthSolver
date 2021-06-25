NEGRO = (0, 0, 0)
GRIS = (160, 160, 160)
CAMINO = (210, 210, 210)
BLANCO = (255,255,255)
VERDE = (0,210,0)
ROJO = (210, 0, 0)
AZUL = (93, 173, 226)
class Celda:
    def __init__(self, valor):
        self.inicial = valor
        self.juego = valor
        self.original = valor
        self.mascara = ""
        if valor == "%":
            self.mascara = "%"
        else:
            self.mascara = "X"

    def setJuego(self, valor):
        self.juego = valor
    def setMascara(self, valor):
        self.mascara = valor
    def paredVisitado(self):
        if self.juego == "0" or self.juego == "V":
            return False
        return True

    def hardReset(self):
        self.juego = self.inicial
        if self.juego == "%":
            self.mascara = "%"
        else:
            self.mascara = "X"

    def resetOriginal(self):
        self.juego = self.original
        self.mascara = "X"

    def resetVisitado(self):
        self.juego = "V"
        self.mascara = "V"

    def setOriginal(self):
        self.original = self.juego

    def setMascara(self, valor):
        self.mascara = valor

    def setJuego2Mascara(self):
        self.mascara = self.juego

    def __str__(self):
        return str(self.juego)

    def isPlayer(self):
        if self.juego == "P":
            return True
        if self.mascara == "P":
            return True
        return False

    def getColor(self, juego):
        color = GRIS
        if juego == False:
            if self.juego == "1":
                color = CAMINO
            elif self.juego == "%":
                color = BLANCO
            elif self.juego == "P":
                color = VERDE
            elif self.juego == "M":
                color = ROJO
            elif self.juego == "X":
                color = NEGRO
            elif self.juego == "V":
                color = AZUL
        else:
            if self.mascara == "1":
                color = CAMINO
            elif self.mascara == "%":
                color = BLANCO
            elif self.mascara == "P":
                color = VERDE
            elif self.mascara == "M":
                color = ROJO
            elif self.mascara == "X":
                color = NEGRO
            elif self.mascara == "V":
                color = AZUL
        return color;